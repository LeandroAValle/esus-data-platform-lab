.PHONY: up down logs ps psql

up:
	docker compose -f docker/docker-compose.yml --env-file docker/.env up -d

down:
	docker compose -f docker/docker-compose.yml --env-file docker/.env down

logs:
	docker compose -f docker/docker-compose.yml --env-file docker/.env logs -f

ps:
	docker compose -f docker/docker-compose.yml --env-file docker/.env ps

psql:
	docker exec -it esus-postgres psql -U esus -d esus

spark-build:
	docker build -t esus-spark -f docker/spark/Dockerfile .

silver: spark-build
	docker run --rm -v "$(CURDIR)":/app -w /app esus-spark -m src.silver.tables_to_silver

gold:
	dbt run --project-dir dbt --profiles-dir dbt

gold-docs:
	dbt docs generate --project-dir dbt --profiles-dir dbt && dbt docs serve --project-dir dbt --profiles-dir dbt

dashboard:
	docker compose -f docker/docker-compose.streamlit.yml up -d --build

export-powerbi:
	docker run --rm -w /app -v "$(CURDIR)":/app -v esus-data:/app/data --entrypoint python docker-streamlit -m src.dashboard.export_powerbi
