"""
Converte a landing zone (data/raw/<tabela>/extraction_date=.../*.parquet)
em tabelas Delta Lake (data/lakehouse/bronze/<tabela>) — a camada Bronze
de fato da arquitetura Lakehouse.

Cada execução relê todas as partições de extraction_date presentes na
landing zone e sobrescreve a tabela Delta correspondente (mode=overwrite),
o que é idempotente: rodar de novo não duplica linhas. O particionamento
por extraction_date é preservado como coluna real na tabela Delta.

Processa arquivo por arquivo (schema primeiro, dados depois) em vez de
concatenar a tabela inteira em memória — ambientes com RAM limitada (ex.:
a VM do Docker Desktop, ~8 GB pra todos os containers) não aguentam
carregar tabelas de milhões de linhas de uma vez (tb_atend, tb_auditoria_
evento etc. já causaram OOM/SIGKILL com a abordagem antiga).

Uso:
    python -m src.bronze.to_delta
"""

import os
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq
from deltalake import write_deltalake
from dotenv import load_dotenv

load_dotenv()


def _normalize_timestamp_tz(schema: pa.Schema) -> pa.Schema:
    """timestamp with time zone do Postgres vira offset fixo (-02:00,
    -03:00 etc.) dependendo do horário de verão no momento da leitura —
    chunks diferentes da mesma coluna acabam com offsets diferentes, o
    que quebra a unificação de schema. Normaliza tudo pra UTC."""
    fields = []
    for field in schema:
        if pa.types.is_timestamp(field.type) and field.type.tz is not None:
            field = field.with_type(pa.timestamp("us", tz="UTC"))
        fields.append(field)
    return pa.schema(fields)


def _fix_null_typed_fields(schema: pa.Schema) -> pa.Schema:
    """Colunas 100% nulas (comuns em chunks pequenas) viram tipo `null`
    no pyarrow, que o Delta Lake não aceita — força string nelas."""
    fields = [f.with_type(pa.string()) if pa.types.is_null(f.type) else f for f in schema]
    return pa.schema(fields)


def _list_part_files(table_raw_dir: Path) -> list[tuple[Path, str]]:
    files = []
    for extraction_dir in sorted(table_raw_dir.glob("extraction_date=*")):
        extraction_date = extraction_dir.name.split("=", 1)[1]
        for part_file in sorted(extraction_dir.glob("part-*.parquet")):
            files.append((part_file, extraction_date))
    return files


def _unified_schema(part_files: list[tuple[Path, str]]) -> pa.Schema:
    """Só lê metadado (schema), nunca os dados, pra descobrir o schema
    unificado — leve mesmo com milhares de arquivos.

    A normalização de timezone precisa rodar em CADA schema individual
    antes do unify_schemas — schemas com offsets diferentes (-02:00 vs
    -03:00, por causa do horário de verão no momento da leitura de cada
    chunk) fazem o próprio unify_schemas falhar, então normalizar só no
    resultado já unificado não adianta."""
    schemas = [_normalize_timestamp_tz(pq.read_schema(f)) for f, _ in part_files]
    unified = pa.unify_schemas(schemas, promote_options="permissive")
    unified = _fix_null_typed_fields(unified)
    return unified.append(pa.field("extraction_date", pa.string()))


def convert_table(table_name: str, raw_dir: Path, lakehouse_dir: Path) -> int:
    table_raw_dir = raw_dir / table_name
    part_files = _list_part_files(table_raw_dir)
    if not part_files:
        return 0

    target_schema = _unified_schema(part_files)
    delta_path = str(lakehouse_dir / "bronze" / table_name)

    total_rows = 0
    for i, (part_file, extraction_date) in enumerate(part_files):
        chunk = pq.read_table(part_file)
        chunk = chunk.append_column(
            "extraction_date", pa.array([extraction_date] * chunk.num_rows, pa.string())
        )
        chunk = chunk.cast(target_schema)
        write_deltalake(
            delta_path,
            chunk,
            mode="overwrite" if i == 0 else "append",
            partition_by=["extraction_date"],
        )
        total_rows += chunk.num_rows

    return total_rows


def main() -> None:
    raw_dir = Path(os.environ.get("RAW_OUTPUT_DIR", "data/raw"))
    lakehouse_dir = Path(os.environ.get("LAKEHOUSE_DIR", "data/lakehouse"))

    tables = sorted(p.name for p in raw_dir.iterdir() if p.is_dir())
    print(f"Convertendo {len(tables)} tabelas de {raw_dir} para Delta Lake em {lakehouse_dir / 'bronze'}")

    failed: list[str] = []
    for i, table in enumerate(tables, 1):
        try:
            rows = convert_table(table, raw_dir, lakehouse_dir)
            print(f"  [{i}/{len(tables)}] {table}: {rows} linhas")
        except Exception as exc:  # partição vazia, parquet sem linhas, etc.
            failed.append(table)
            print(f"  [{i}/{len(tables)}] {table}: FALHOU ({exc})")

    if failed:
        print(f"\n{len(failed)} tabelas falharam: {', '.join(failed)}")

    print("Concluído.")


if __name__ == "__main__":
    main()
