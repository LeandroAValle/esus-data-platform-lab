"""
Exporta as tabelas Gold (gold.duckdb) para Parquet numa pasta acessível
pelo Windows host — Power BI Desktop não roda em container e não
enxerga o named volume esus-data, então isso vira a ponte.

Power BI: Obter Dados > Pasta (aponta pra exports/powerbi/) ou
Obter Dados > Parquet (arquivo por arquivo). Um refresh no Power BI
sempre relê o Parquet mais recente gerado aqui.

Uso: python -m src.dashboard.export_powerbi
"""

import os
from pathlib import Path

import duckdb

GOLD_DB_PATH = os.environ.get("GOLD_DB_PATH", "data/lakehouse/gold.duckdb")
EXPORT_DIR = Path(os.environ.get("POWERBI_EXPORT_DIR", "exports/powerbi"))

GOLD_TABLES = [
    "gold_hipertensos",
    "gold_diabeticos",
    "gold_cobertura_vacinal",
    "gold_acompanhamento_pre_natal",
    "gold_producao_por_ubs",
    "gold_producao_por_equipe",
    "gold_visitas_domiciliares",
]


def main() -> None:
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(GOLD_DB_PATH, read_only=True)

    for table in GOLD_TABLES:
        out_path = EXPORT_DIR / f"{table}.parquet"
        con.sql(f"COPY (SELECT * FROM main_gold.{table}) TO '{out_path}' (FORMAT PARQUET)")
        rows = con.sql(f"SELECT count(*) FROM main_gold.{table}").fetchone()[0]
        print(f"  {table} -> {out_path} ({rows} linhas)")

    print(f"\nExportado pra {EXPORT_DIR}. No Power BI Desktop: Obter Dados > Pasta > {EXPORT_DIR.resolve()}")


if __name__ == "__main__":
    main()
