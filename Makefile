pyright: ## Runs pyright
	@./scripts/pyright

isort: ## Runs isort
	@./scripts/isort .

black: ## Runs black
	@./scripts/black .

lint: ## Runs linting tools
	@./scripts/lint

lint-fix: ## Runs a linting pipeline with auto fixing: black, isort, ruff, and mypy
	@./scripts/lint --fix

install: ## Installs the project (only main dependencies)
	@./scripts/install --only main

install-dev: ## Installs the project (with dev dependencies)
	@./scripts/install --only main,dev

ruff: ## Runs ruff
	@./scripts/ruff

model-serve: ## Serves the model in local environment
	@./scripts/serve-model "./artifacts/models/churn/model.flm" \
		--app-title "Churn classifier" \
		--app-description "Predict whether a customer will leave a company or not" \
		--app-version "1.0.0"

model-start: ## Start serving the model container 
	@./scripts/start-model

model-stop: ## Stop serving the model container
	@./scripts/stop-model

airflow-start: ## Start serving airflow
	@./scripts/start-airflow

airflow-stop: ## Start serving airflow
	@./scripts/stop-airflow

test: ## Runs tests
	@./scripts/test

.PHONY: help pyright isort black lint lint-fix install install-dev
.DEFAULT_GOAL := help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
