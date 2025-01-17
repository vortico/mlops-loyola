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
3. Run the linting checks:
```bash
make lint
```
4. Start the model server:
```bash
make serve-model
```

## 📚 Repository Documentation

You can find the documentation in the `docs/` directory:

- `docs/` - Detailed documentation
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
make help                 # Show all available commands
make install              # Install all dependencies
make lint                 # Run all linting tools
make lint-fix            # Auto-fix common issues
make test                # Run test suite
make serve-model         # Start the model server
make serve-airflow       # Start the airflow server
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