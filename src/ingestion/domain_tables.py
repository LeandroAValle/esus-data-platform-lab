"""
Descobre as tabelas de domínio/lookup (tb_*, rl_*) da base e-SUS em
runtime e classifica colunas por heurística de nome (ver
PII_NAME_PATTERNS_* em pii_config.py). São ~700+ tabelas majoritariamente
de código/descrição, então não fazem sentido revisar uma a uma — mas o
mesmo cuidado de hash/drop se aplica caso alguma tenha coluna sensível.
"""

import pandas as pd
from sqlalchemy.engine import Engine

from src.ingestion.pii_config import (
    PII_NAME_KEYWORDS_ON_NO_PREFIX,
    PII_NAME_PATTERNS_DROP,
    PII_NAME_PATTERNS_HASH,
)

DISCOVER_TABLES_QUERY = """
SELECT tablename FROM pg_tables
WHERE schemaname = 'public'
  AND left(tablename, 3) IN ('tb_', 'rl_')
ORDER BY tablename;
"""

TABLE_COLUMNS_QUERY = """
SELECT column_name FROM information_schema.columns
WHERE table_schema = 'public' AND table_name = %(table)s;
"""


def discover_domain_tables(engine: Engine) -> list[str]:
    df = pd.read_sql(DISCOVER_TABLES_QUERY, engine)
    return df["tablename"].tolist()


def classify_columns(engine: Engine, table: str) -> dict[str, list[str]]:
    cols_df = pd.read_sql(TABLE_COLUMNS_QUERY, engine, params={"table": table})
    columns = cols_df["column_name"].tolist()

    hash_cols = [c for c in columns if any(p in c for p in PII_NAME_PATTERNS_HASH)]
    drop_cols = [
        c
        for c in columns
        if any(p in c for p in PII_NAME_PATTERNS_DROP)
        or (c.startswith("no_") and any(k in c for k in PII_NAME_KEYWORDS_ON_NO_PREFIX))
    ]
    return {"hash": hash_cols, "drop": drop_cols}
