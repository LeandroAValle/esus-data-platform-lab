"""
DAG do pipeline completo eSUS Data Platform: Postgres (fonte) -> Bronze
(raw parquet) -> Bronze (Delta Lake) -> Silver (PySpark) -> Gold (dbt)
-> export Power BI (Parquet em exports/powerbi/, pasta do host).

Extração e conversão pra Delta rodam direto no container do Airflow
(dependências leves: psycopg2, pandas, pyarrow, deltalake). Silver e Gold
disparam containers-irmãos via Docker socket (DockerOperator), reusando
a imagem esus-spark (tem PySpark e dbt) já construída no sprint 04/05 —
ver docker/spark/Dockerfile e `make spark-build`.

Trigger manual (schedule=None) — não roda sozinho contra a base de
produção sem alguém decidir isso.
"""

import os
from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

PROJECT_HOST_PATH = os.environ.get("PROJECT_HOST_PATH", "")
SPARK_IMAGE = os.environ.get("SPARK_IMAGE", "esus-spark")
STREAMLIT_IMAGE = os.environ.get("STREAMLIT_IMAGE", "docker-streamlit")

project_mount = Mount(source=PROJECT_HOST_PATH, target="/app", type="bind")
# mesmo named volume "esus-data" usado pelo container do Airflow — ver
# nota em docker/docker-compose.airflow.yml sobre a race de bind-mount
# Windows com escrita Delta (Rust/delta-rs).
data_mount = Mount(source="esus-data", target="/app/data", type="volume")

with DAG(
    dag_id="esus_pipeline",
    description="Postgres -> Bronze -> Delta -> Silver -> Gold",
    schedule=None,
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["esus", "lakehouse"],
) as dag:
    extract_bronze = BashOperator(
        task_id="extract_bronze",
        bash_command="cd /opt/airflow/project && python -m src.ingestion.extract_to_bronze",
    )

    to_delta = BashOperator(
        task_id="bronze_to_delta",
        bash_command="cd /opt/airflow/project && python -m src.bronze.to_delta",
    )

    silver = DockerOperator(
        task_id="silver_transform",
        image=SPARK_IMAGE,
        entrypoint=["python"],
        command=["-m", "src.silver.tables_to_silver"],
        working_dir="/app",
        mounts=[project_mount, data_mount],
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        auto_remove="success",
        mount_tmp_dir=False,
    )

    gold = DockerOperator(
        task_id="gold_dbt_run",
        image=SPARK_IMAGE,
        entrypoint=["dbt"],
        command=["run", "--project-dir", "dbt", "--profiles-dir", "dbt"],
        working_dir="/app",
        mounts=[project_mount, data_mount],
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        auto_remove="success",
        mount_tmp_dir=False,
    )

    export_powerbi = DockerOperator(
        task_id="export_powerbi",
        image=STREAMLIT_IMAGE,
        entrypoint=["python"],
        command=["-m", "src.dashboard.export_powerbi"],
        working_dir="/app",
        mounts=[project_mount, data_mount],
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        auto_remove="success",
        mount_tmp_dir=False,
    )

    extract_bronze >> to_delta >> silver >> gold >> export_powerbi
