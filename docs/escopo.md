# Escopo Oficial do Projeto — eSUS Data Platform

> Transcrito de `eSUS_Data_Platform_Escopo_Final.pdf`.

## 1. Visão do projeto

**Nome:** eSUS Data Platform

**Objetivo:** Construir uma plataforma moderna de Engenharia de Dados capaz de transformar dados operacionais do e-SUS em dados tratados, confiáveis e indicadores estratégicos para apoio à gestão da Atenção Primária à Saúde.

O projeto será desenvolvido como um case profissional de Data Engineering, utilizando arquitetura Lakehouse e práticas de ETL/ELT, processamento distribuído, orquestração, qualidade de dados, cloud e DataOps.

Também servirá como base para uma série de laboratórios arquiteturais, nos quais os mesmos problemas serão implementados utilizando tecnologias alternativas de mercado.

## 2. Problema de negócio

- Acompanhamento de pré-natal
- Vacinação
- Hipertensos
- Diabéticos
- Produção por UBS
- Produção por equipe
- Visitas domiciliares
- Metas da APS

**Foco:** estudo e portfólio; demonstrações públicas usam dados sintéticos. Fontes reais exigem autorização e controles de acesso.

## 3. Arquitetura principal

```
e-SUS PostgreSQL
  ↓
Python / Ingestion
  ↓
Bronze (Delta Lake)
  ↓
Silver (PySpark / Spark SQL)
  ↓
Gold (dbt / Delta)
  ↓
Dashboard (Streamlit / Power BI)
```

- Orquestração: Apache Airflow
- Qualidade: Great Expectations

## 4. Stack principal

- **Dados:** PostgreSQL, SQL Server, SQL, Delta Lake, Data Lake, Lakehouse
- **Processamento:** Python, PySpark, Apache Spark, Spark SQL, Databricks
- **Transformação:** dbt, SQL, PySpark
- **Orquestração:** Apache Airflow
- **Data Quality:** Great Expectations, testes automatizados, validação de schema, duplicidade, nulos, integridade referencial
- **DevOps / DataOps:** Git, GitHub, GitHub Actions, Docker
- **Cloud:** Azure Data Lake Storage Gen2, Azure Data Factory, Databricks, Azure Blob Storage, AWS S3, IAM

## 5. Backlog principal — 12 Sprints

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

## 6. Camadas do Lakehouse

- **Bronze:** Dados brutos preservados para reprocessamento e histórico.
- **Silver:** Limpeza, padronização, deduplicação e regras de negócio.
- **Gold:** Tabelas analíticas e indicadores prontos para consumo.

## 7. Streaming

```
Evento de alteração
  ↓
Kafka
  ↓
Consumer
  ↓
PySpark
  ↓
Delta Lake
  ↓
Indicadores APS
```

## 8. Dashboard

Streamlit inicialmente e Power BI posteriormente, com filtros por município, UBS, equipe, profissional, período e indicador.

## 9. Laboratórios Arquiteturais

- **LAB 01 — AWS Data Lake:** S3 + IAM + Spark
- **LAB 02 — Azure Data Platform:** ADLS Gen2 + Data Factory + Databricks
- **LAB 03 — GCP / BigQuery:** Cloud Storage + BigQuery
- **LAB 04 — Snowflake:** Warehouse analítico com dbt
- **LAB 05 — Kafka Streaming:** Event Streaming em tempo real
- **LAB 06 — Terraform:** Infrastructure as Code
- **LAB 07 — Kubernetes:** Orquestração de containers
- **LAB 08 — Observabilidade:** OpenTelemetry + Prometheus + Grafana

### Regra dos Labs

Nenhum laboratório existe apenas para adicionar tecnologia ao currículo. Cada um deve explicar: qual problema resolve, como se encaixa na arquitetura e quais são seus trade-offs.

## 10. Papéis

- **Claude:** Engenheiro de Dados Implementador — escreve código, notebooks, pipelines, Airflow, Docker, testes, CI/CD e documentação.
- **ChatGPT:** Tech Lead / Arquiteto — define arquitetura, revisa decisões, explica conceitos, prioriza backlog e prepara para entrevistas.
- **Leandro:** Desenvolvedor e Engenheiro de Dados em formação — compreender e defender tecnicamente cada sprint.

## 11. Resultado Final

O projeto demonstrará competências em ETL/ELT, Lakehouse, Databricks, PySpark, Spark, Airflow, dbt, Delta Lake, Data Quality, Kafka, Docker, GitHub Actions, Azure, AWS, Terraform, Kubernetes, Observabilidade e Analytics aplicado à Saúde.
