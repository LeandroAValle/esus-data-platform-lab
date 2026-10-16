# eSUS Data Platform Lab

**Laboratório de Engenharia de Dados: PostgreSQL → Bronze Delta → Silver PySpark → Gold dbt → análise.**

[![Explorar arquitetura](https://img.shields.io/badge/Explorar-arquitetura%20interativa-9de4e7?style=for-the-badge&labelColor=112c45)](https://leandroavalle.github.io/esus-data-platform-lab/)
[![CI](https://github.com/LeandroAValle/esus-data-platform-lab/actions/workflows/verify.yml/badge.svg)](https://github.com/LeandroAValle/esus-data-platform-lab/actions/workflows/verify.yml)

![Prévia da arquitetura do laboratório](docs/architecture-preview.png)

> **Projeto em desenvolvimento.** O código de ingestão, processamento, modelos, orquestração e consumo está presente neste repositório. A vitrine online usa apenas metadados do código, sem executar o pipeline nem exibir dados de saúde.

## Veja primeiro

| Recurso | Acesso |
| --- | --- |
| Visão interativa das camadas | [Abrir a vitrine](https://leandroavalle.github.io/esus-data-platform-lab/) |
| DAG manual de ponta a ponta | [`dags/esus_pipeline_dag.py`](dags/esus_pipeline_dag.py) |
| Modelos analíticos | [`dbt/models/marts/`](dbt/models/marts/) |
| Política de publicação e privacidade | [Publicação segura](docs/PUBLICATION.md) |
| Decisões e limitações | [Arquitetura](docs/ARCHITECTURE.md) · [Indicadores Gold](docs/gold.md) |

### Estado verificado no código

| Componente | Situação |
| --- | --- |
| Ingestão PostgreSQL → Parquet | Implementação presente; requer fonte configurada e autorizada |
| Bronze Delta Lake | Implementação presente |
| Silver PySpark | Implementação presente; execução prevista em contêiner |
| Gold dbt/DuckDB | 7 modelos analíticos presentes |
| Orquestração Airflow | DAG de 5 tarefas presente, com acionamento manual |
| Streamlit e exportação Power BI | Código presente |
| Great Expectations, Kafka, AWS e Azure | Estudos planejados; não apresentados como implementados |

**Privacidade:** hash com salt e remoção de colunas são medidas de pseudonimização/redução de dados, não garantia automática de anonimização. Dados de saúde exigem autorização, acesso controlado e revisão de privacidade. A cópia pública foi criada com histórico novo, sem `.env`, dados locais ou exports do laboratório privado.

### Verificação local sem dados de saúde

Com Python 3.11+ e `pandas==2.2.2`:

```bash
python -m unittest discover -s tests -v
python -m compileall -q src dags
python -m http.server 8000 --directory site
```

Abra `http://localhost:8000` para explorar a arquitetura. Estes comandos não se conectam a banco. Para executar o pipeline completo é necessária uma fonte e-SUS autorizada, configuração local em `.env` e revisão de privacidade; a base sintética mínima de `docker/postgres/init/` valida apenas o ambiente Docker e não substitui o esquema e-SUS usado pela ingestão.

---

Plataforma de Engenharia de Dados que transforma dados operacionais do e-SUS em dados tratados, confiáveis e indicadores estratégicos para apoio à gestão da Atenção Primária à Saúde (APS).

Case de Data Engineering usando arquitetura Lakehouse (Bronze/Silver/Gold), ETL/ELT, processamento distribuído e orquestração. Qualidade ampliada, cloud e DataOps seguem em evolução.

> Use dados sintéticos ou uma fonte expressamente autorizada e protegida. Projeto de estudo/portfólio.

## Arquitetura

```
e-SUS PostgreSQL
  → Python / Ingestion
  → Bronze (Delta Lake)
  → Silver (PySpark / Spark SQL)
  → Gold (dbt / DuckDB)
  → Dashboard (Streamlit / Power BI)
```

Orquestração: Apache Airflow · Qualidade automatizada ampliada: planejada

## Estrutura

```
docker/          # docker-compose, Dockerfiles
src/
  ingestion/      # extração PostgreSQL e-SUS -> landing zone (parquet + redução de PII)
  bronze/         # landing zone -> Delta Lake (camada Bronze)
  silver/         # limpeza, padronização, dedup (PySpark)
  gold/           # reservado; modelos dbt ficam em dbt/models/
dags/             # DAGs do Airflow
notebooks/        # exploração e prototipagem
tests/            # testes focados de privacidade e vitrine
data/
  raw/             # landing zone (parquet particionado por extraction_date) — não versionado
  lakehouse/       # Delta Lake: bronze/, silver/, gold/ — não versionado
docs/             # escopo, decisões de arquitetura, dicionário de dados
```

Pipeline até agora: `src/ingestion/extract_to_bronze.py` (Postgres → `data/raw/`,
pseudonimizado) → `src/bronze/to_delta.py` (`data/raw/` → `data/lakehouse/bronze/`,
Delta Lake real com transaction log e schema) → `src/silver/tables_to_silver.py`
(Bronze → `data/lakehouse/silver/`, limpeza/padronização/dedup via PySpark,
rodando em container Docker — ver `make silver`; Windows local não roda PySpark
sem winutils.exe, por isso o processamento vai pro container) → `dbt/`
(Silver/Bronze → `gold.duckdb`, indicadores analíticos via `make gold`; ver
[docs/gold.md](docs/gold.md)). Inspecionar uma tabela Delta:
`python -m src.bronze.delta_info <tabela>`.

## Plano de trabalho — 12 sprints

| Sprint | Entrega |
|---|---|
| 01 | Docker + ambiente |
| 02 | PostgreSQL → Bronze |
| 03 | Delta Lake + arquitetura Lakehouse |
| 04 | PySpark + camada Silver |
| 05 | dbt + camada Gold |
| 06 | Indicadores APS |
| 07 | Airflow + DAGs |
| 08 | Kafka + laboratório de streaming |
| 09 | Azure ADLS + integração cloud |
| 10 | AWS S3 + laboratório de Data Lake |
| 11 | Great Expectations + Data Quality |
| 12 | GitHub Actions + CI/CD + documentação |

Ver escopo completo em [docs/escopo.md](docs/escopo.md).

## Laboratórios arquiteturais

Há estudos planejados com AWS, Azure, GCP/BigQuery, Snowflake, Kafka, Terraform, Kubernetes e observabilidade. Eles ainda não são apresentados como implementações concluídas. Ver [docs/escopo.md](docs/escopo.md#9-laboratórios-arquiteturais).

## Power BI

Power BI Desktop roda no Windows nativo, fora do Docker, e não enxerga o
named volume onde vive o `gold.duckdb`. Ponte: `make export-powerbi`
exporta as 7 tabelas Gold pra `exports/powerbi/*.parquet` (pasta comum do
host) — no Power BI: **Obter Dados > Pasta** apontando pra essa pasta, ou
**Obter Dados > Parquet** arquivo por arquivo. Quando a DAG é acionada manualmente,
o código prevê esse export como último passo (`export_powerbi`).

## Stack

**Código presente:** PostgreSQL, Delta Lake, Python, PySpark, dbt, DuckDB, Apache Airflow, Docker, Streamlit e exportação Parquet. **Roadmap:** Great Expectations, Kafka, serviços Azure/AWS e observabilidade. GitHub Actions verifica testes e sintaxe desta cópia pública.
