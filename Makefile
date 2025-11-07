.PHONY: dev up down run test lint format typecheck api gen-client docker-build docker-run

PY=python
UV?=uv
VENV=.venv

dev:
	@($(UV) venv || $(PY) -m venv $(VENV)) && . $(VENV)/bin/activate && pip install -U pip $(UV) && $(UV) pip install -r requirements.txt

up:
	docker compose up -d

down:
	docker compose down -v

run:
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

test:
	pytest -q

lint:
	ruff check .

format:
	ruff format .

typecheck:
	mypy .

api:
	$(PY) scripts/emit_openapi.py > openapi.json

gen-client:
	openapi-python-client generate --path openapi.json --meta

docker-build:
	docker build -t ${APP_NAME:-aws-fastapi-starter}:dev -f docker/Dockerfile .

docker-run:
	docker run --rm -p 8000:8000 ${APP_NAME:-aws-fastapi-starter}:dev
