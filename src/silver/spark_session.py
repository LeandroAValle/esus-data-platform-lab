from delta import configure_spark_with_delta_pip
from pyspark.sql import SparkSession


def build_spark_session(app_name: str = "esus-silver") -> SparkSession:
    builder = (
        SparkSession.builder.appName(app_name)
        .master("local[*]")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .config("spark.driver.memory", "4g")
        # dados legados do e-SUS têm datas-sentinela inválidas (ex.: ano -1);
        # sem isso o Spark recusa a leitura por segurança de rebase de
        # calendário. Lemos como está e limpamos depois (ver clean.sanitize_date_range).
        .config("spark.sql.parquet.datetimeRebaseModeInRead", "CORRECTED")
        .config("spark.sql.parquet.int96RebaseModeInRead", "CORRECTED")
    )
    return configure_spark_with_delta_pip(builder).getOrCreate()
