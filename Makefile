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
	@./scripts/install --with dev

ruff: ## Runs ruff
	@./scripts/ruff

serve-model: ## Serves the model
	@./scripts/serve-model "./artifacts/models/churn/model.flm" \
		--app-title "Churn classifier" \
		--app-description "Predict whether a customer will leave a company or not" \
		--app-version "1.0.0"

serve-airflow: ## Serves the airflow
	@./scripts/serve-airflow

test: ## Runs tests
	@./scripts/test

.PHONY: help pyright isort black lint lint-fix install install-dev
.DEFAULT_GOAL := help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
