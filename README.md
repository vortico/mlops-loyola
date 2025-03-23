# MLOps and ML Engineering Course

> Loyola University Sevilla

## Overview

Welcome to the MLOps and ML Engineering course! This repository contains practical materials and examples for learning modern Machine Learning Operations (MLOps) and engineering best practices. The course is designed to bridge the gap between data science and production-ready ML systems.

## 🚀 Quick Start

1. Clone this repository

2. Install dependencies:

```bash
make install-dev
```

3. Start the model server

```bash
make model-serve
```

## 📚 Repository Documentation

You can find the documentation in the [`docs/`](./docs/) directory:

- `cicd/` - CI/CD pipeline implementation and practices
- `dev-env/` - Python environment management with pyenv and poetry
- `make/` - Automation and Makefile usage guide
- `package/` - MLOps package structure and implementation
- `airflow/` - Airflow DAGs and configuration
- `mlflow/` - MLflow configuration and best practices
- `package/` - MLOps package structure and implementation

## 🛠 Development Tools

This project uses modern Python development tools and practices:

### Key Make Commands

```bash
airflow-start                  Start serving airflow
airflow-stop                   Start serving airflow
black                          Runs black
install-dev                    Installs the project (with dev dependencies)
install                        Installs the project (only main dependencies)
isort                          Runs isort
lint-fix                       Runs a linting pipeline with auto fixing: black, isort, ruff, and mypy
lint                           Runs linting tools
model-serve                    Serves the model in local environment
model-start                    Start serving the model container
model-stop                     Stop serving the model container
pyright                        Runs pyright
ruff                           Runs ruff
test                           Runs tests
```

### Development Environment

- **Python Version**: 3.13
- **Package Management**: Poetry
- **Code Quality**: black, isort, ruff, pyright
- **Testing**: pytest
- **Model Serving**: Flama
- **Model Deployment**: Docker
- **Model Registry**: mlflow
- **Orchestration**: airflow

## 🎯 Learning Objectives

This course covers:

- Setting up professional ML development environments
- Implementing CI/CD for ML projects
- Building production-ready ML pipelines
- Best practices for model deployment
- Code quality and testing in ML projects

## 📖 Documentation

Detailed documentation is available in the `docs/` directory:

- [CI/CD Implementation](docs/cicd/README.md)
- [Development Environment Setup](docs/dev-env/README.md)
- [Make and Automation](docs/make/README.md)
- [Package Structure](docs/package/README.md)

## 🤝 Contributing

1. Ensure you have all development dependencies installed
2. Make your changes
3. Run the full test suite:

```bash
make lint && make test
```

4. Submit your pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
