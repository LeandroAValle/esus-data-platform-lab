"""
Lê tabelas Delta da camada Bronze, aplica limpeza/padronização/dedup
(src/silver/clean.py) e grava a camada Silver em Delta Lake.

Uso (dentro do container com PySpark — ver Makefile `make silver`):
    python -m src.silver.tables_to_silver
"""

import os
from pathlib import Path

from src.silver.clean import clean_table
from src.silver.spark_session import build_spark_session

# nome_silver -> (tabela_bronze, colunas de chave de negócio)
SILVER_TABLES: dict[str, tuple[str, list[str]]] = {
    "cidadao": ("tb_cidadao", ["co_seq_cidadao"]),
    "unidade_saude": ("tb_unidade_saude", ["co_seq_unidade_saude"]),
    "equipe": ("tb_equipe", ["co_seq_equipe"]),
    "profissional": ("tb_prof", ["co_seq_prof"]),
    "lotacao": ("tb_lotacao", ["co_unico_lotacao"]),
    "atendimento": ("tb_atend", ["co_seq_atend"]),
    "atendimento_profissional": ("tb_atend_prof", ["co_seq_atend_prof"]),
    "vacinacao": ("tb_registro_vacinacao", ["co_seq_registro_vacinacao"]),
    "pre_natal": ("tb_pre_natal", ["co_seq_pre_natal"]),
    "visita_domiciliar": ("tb_visita_domiciliar_acs", ["co_seq_visita_domiciliar_acs"]),
    "problema": ("tb_problema", ["co_seq_problema"]),
    "condicoes_saude_auto": ("tb_condicoes_saude_auto", ["co_seq_condicoes_saude_auto"]),
}


def main() -> None:
    lakehouse_dir = Path(os.environ.get("LAKEHOUSE_DIR", "data/lakehouse"))
    spark = build_spark_session()

    for silver_name, (bronze_table, key_cols) in SILVER_TABLES.items():
        bronze_path = str(lakehouse_dir / "bronze" / bronze_table)
        silver_path = str(lakehouse_dir / "silver" / silver_name)

        df = spark.read.format("delta").load(bronze_path)
        clean_df = clean_table(df, key_cols)

        clean_df.write.format("delta").mode("overwrite").save(silver_path)
        rows = clean_df.count()
        print(f"  {bronze_table} -> silver.{silver_name}: {rows} linhas")

    spark.stop()
    print("Concluído.")


if __name__ == "__main__":
    main()
