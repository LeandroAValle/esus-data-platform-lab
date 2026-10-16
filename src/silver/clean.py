"""Transformações genéricas de limpeza aplicadas na camada Silver."""

from pyspark.sql import DataFrame, Window
from pyspark.sql import functions as F
from pyspark.sql.types import DateType, StringType, TimestampType


def trim_string_columns(df: DataFrame) -> DataFrame:
    for field in df.schema.fields:
        if isinstance(field.dataType, StringType):
            df = df.withColumn(field.name, F.trim(F.col(field.name)))
    return df


def dedupe_latest(df: DataFrame, key_cols: list[str], order_col: str = "extraction_date") -> DataFrame:
    """Mantém apenas a versão mais recente (maior extraction_date) por chave de negócio."""
    window = Window.partitionBy(*key_cols).orderBy(F.col(order_col).desc())
    return (
        df.withColumn("_rn", F.row_number().over(window))
        .filter(F.col("_rn") == 1)
        .drop("_rn")
    )


def sanitize_date_range(df: DataFrame, min_year: int = 1900, max_year: int = 2100) -> DataFrame:
    """Datas-sentinela inválidas do e-SUS legado (ex.: ano -1, ano 9999)
    viram NULL em vez de derrubar o pipeline ou poluir os indicadores."""
    for field in df.schema.fields:
        if isinstance(field.dataType, (DateType, TimestampType)):
            col = F.col(field.name)
            year = F.year(col)
            df = df.withColumn(
                field.name,
                F.when((year < min_year) | (year > max_year), None).otherwise(col),
            )
    return df


def clean_table(df: DataFrame, key_cols: list[str]) -> DataFrame:
    df = trim_string_columns(df)
    df = sanitize_date_range(df)
    df = dedupe_latest(df, key_cols)
    return df.dropDuplicates()
