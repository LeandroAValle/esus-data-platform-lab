"""
Gera docs/dicionario_dados.md a partir dos comentários (COMMENT ON)
nativos do schema e-SUS de origem, para as tabelas usadas na ingestão.

Uso:
    python -m src.ingestion.dump_metadata
"""

from pathlib import Path

import pandas as pd

from src.ingestion.db import source_engine
from src.ingestion.pii_config import TABLES

COLUMN_COMMENT_QUERY = """
SELECT
    a.attname AS coluna,
    format_type(a.atttypid, a.atttypmod) AS tipo,
    pgd.description AS descricao
FROM pg_catalog.pg_statio_all_tables st
JOIN pg_catalog.pg_attribute a ON a.attrelid = st.relid
LEFT JOIN pg_catalog.pg_description pgd
    ON pgd.objoid = st.relid AND pgd.objsubid = a.attnum
WHERE st.relname = %(table)s
  AND a.attnum > 0
  AND NOT a.attisdropped
ORDER BY a.attnum;
"""

TABLE_COMMENT_QUERY = """
SELECT d.description
FROM pg_class c
JOIN pg_description d ON d.objoid = c.oid AND d.objsubid = 0
WHERE c.relname = %(table)s;
"""


def main() -> None:
    engine = source_engine()
    lines = [
        "# Dicionário de Dados — Bronze (fonte: e-SUS)",
        "",
        "Gerado a partir dos metadados nativos (`COMMENT ON`) do schema de origem.",
        "Colunas marcadas com `[hash]` ou `[drop]` foram pseudonimizadas/removidas na Bronze — ver [src/ingestion/pii_config.py](../src/ingestion/pii_config.py). Isso não garante anonimização do conjunto.",
        "",
    ]

    for table, columns_cfg in TABLES.items():
        hash_cols = set(columns_cfg.get("hash", []))
        drop_cols = set(columns_cfg.get("drop", []))

        table_comment_df = pd.read_sql(TABLE_COMMENT_QUERY, engine, params={"table": table})
        table_comment = table_comment_df.iloc[0, 0] if not table_comment_df.empty else None

        lines.append(f"## {table}")
        if table_comment:
            lines.append(f"\n{table_comment}\n")
        lines.append("| Coluna | Tipo | Descrição | Bronze |")
        lines.append("|---|---|---|---|")

        cols_df = pd.read_sql(COLUMN_COMMENT_QUERY, engine, params={"table": table})
        for _, row in cols_df.iterrows():
            coluna = row["coluna"]
            status = "drop" if coluna in drop_cols else ("hash" if coluna in hash_cols else "mantida")
            descricao = (row["descricao"] or "").replace("\n", " ").replace("|", "\\|")
            lines.append(f"| {coluna} | {row['tipo']} | {descricao} | {status} |")

        lines.append("")

    output_path = Path("docs/dicionario_dados.md")
    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Escrito {output_path} ({len(TABLES)} tabelas)")


if __name__ == "__main__":
    main()
