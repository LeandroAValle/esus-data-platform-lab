"""
Extrai tabelas selecionadas da base e-SUS de origem, pseudonimiza identificadores
sensíveis e grava como Parquet na landing zone (data/raw/<tabela>/).
Conversão para Delta Lake (camada Bronze) fica em src/bronze/to_delta.py.

Uso:
    python -m src.ingestion.extract_to_bronze
"""

import datetime as dt
import os
from pathlib import Path

import pandas as pd

from src.ingestion.anonymize import anonymize_dataframe
from src.ingestion.db import source_engine
from src.ingestion.domain_tables import classify_columns, discover_domain_tables
from src.ingestion.pii_config import TABLES

CHUNK_SIZE = 50_000


def _row_limit() -> int | None:
    raw = os.environ.get("INGESTION_ROW_LIMIT", "").strip()
    return int(raw) if raw else None


def extract_table(
    table: str, columns_cfg: dict, engine, output_dir: Path, extraction_date: str, apply_limit: bool = True
) -> int:
    limit = _row_limit() if apply_limit else None
    query = f"SELECT * FROM {table}"
    if limit:
        query += f" LIMIT {limit}"

    table_dir = output_dir / table / f"extraction_date={extraction_date}"
    success_marker = table_dir / "_SUCCESS"
    if success_marker.exists():
        return -1  # já extraído nesta data — pula (retomada após interrupção)
    table_dir.mkdir(parents=True, exist_ok=True)

    total_rows = 0
    # stream_results=True força cursor server-side no psycopg2 — sem isso,
    # pd.read_sql(chunksize=...) ainda baixa a tabela inteira pra memória
    # antes de fatiar em chunks, e tabelas grandes (ex.: tb_auditoria_evento,
    # 12M linhas) estouram RAM do container e o processo é morto (SIGKILL).
    with engine.connect().execution_options(stream_results=True, yield_per=CHUNK_SIZE) as conn:
        for part_num, chunk in enumerate(pd.read_sql(query, conn, chunksize=CHUNK_SIZE)):
            chunk = anonymize_dataframe(chunk, columns_cfg.get("hash", []), columns_cfg.get("drop", []))
            chunk.to_parquet(table_dir / f"part-{part_num:05d}.parquet", index=False)
            total_rows += len(chunk)

    success_marker.touch()
    return total_rows


def main() -> None:
    output_dir = Path(os.environ.get("RAW_OUTPUT_DIR", "data/raw"))
    extraction_date = dt.date.today().isoformat()
    engine = source_engine()

    print(f"Extraindo {len(TABLES)} tabelas operacionais (curadas) para {output_dir} (extraction_date={extraction_date})")
    for table, columns_cfg in TABLES.items():
        rows = extract_table(table, columns_cfg, engine, output_dir, extraction_date)
        print(f"  {table}: {'já extraída, pulada' if rows == -1 else f'{rows} linhas'}")

    domain_tables = discover_domain_tables(engine)
    print(f"\nExtraindo {len(domain_tables)} tabelas de domínio/lookup (tb_*, rl_*), sem limite de linhas")
    failed: list[str] = []
    for i, table in enumerate(domain_tables, 1):
        try:
            columns_cfg = classify_columns(engine, table)
            rows = extract_table(table, columns_cfg, engine, output_dir, extraction_date, apply_limit=False)
            flag = " (PII heurística aplicada)" if columns_cfg["hash"] or columns_cfg["drop"] else ""
            status = "já extraída, pulada" if rows == -1 else f"{rows} linhas{flag}"
            print(f"  [{i}/{len(domain_tables)}] {table}: {status}")
        except Exception as exc:  # dado sujo na fonte não pode derrubar as demais 700+ tabelas
            failed.append(table)
            print(f"  [{i}/{len(domain_tables)}] {table}: FALHOU ({exc})")

    if failed:
        print(f"\n{len(failed)} tabelas falharam (ver acima): {', '.join(failed)}")

    print("Concluído.")


if __name__ == "__main__":
    main()
