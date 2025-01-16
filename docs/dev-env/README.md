# Python Environment Management

## Overview

This project uses modern Python environment management tools to ensure consistency and reproducibility:
- [**pyenv**](https://github.com/pyenv/pyenv): Manages Python versions
- [**poetry**](https://python-poetry.org/): Handles dependencies and virtual environments
- [**pyproject.toml**](https://www.python.org/dev/peps/pep-0518/): Configures project settings and tools

If you prefer using [**conda**](https://docs.conda.io/en/latest/), you can use the [**conda**](https://github.com/conda/conda) environment. However, we recommend using pyenv and poetry for this project, as it is more flexible and easier to manage.
When working with `conda`, don't forget to run `conda activate <environment-name>` to activate the environment, and install poetry with `pip install poetry`.

## Python Version Management with pyenv

[pyenv](https://github.com/pyenv/pyenv) allows you to install and switch between multiple Python versions.

### Basic pyenv Commands

- `pyenv install 3.13.1`: Install a specific Python version
- `pyenv global 3.13.1`: Set a global Python version
- `pyenv local 3.13.1`: Set a local Python version for the current directory
- `pyenv versions`: List installed Python versions
- `pyenv shell 3.13.1`: Activate a specific Python version in the current shell


## Package Management with Poetry

[`poetry`](https://python-poetry.org/) is a tool for dependency management and packaging in Python. It helps you declare, manage, and install dependencies of Python projects.

### Basic Poetry Commands

- `poetry install`: Install dependencies
- `poetry add <package-name>`: Add a dependency
- `poetry add <package-name> --group dev`: Add a dependency to the development group
- `poetry remove <package-name>`: Remove a dependency
- `poetry update <package-name>`: Update a dependency

### pyenv and Poetry Integration

[`poetry`](https://python-poetry.org/) uses `pyenv` to manage Python versions. When you run `poetry install`, it will use the global Python version set by `pyenv`.

### Locate the Python Environment

To find the Python environment, run `poetry env info --path`. This will show you the path to the virtual environment.

We recommend configuring poetry so that the virtual environment is located in the project root. This can be done by running:

```bash
poetry config virtualenvs.in-project true
```

or by adding the following to your `pyproject.toml` file:

```toml
[tool.poetry]
virtualenvs.in-project = true
```

This will create the virtual environment in the project root, and you can find it by running `poetry env info --path`.

## Additional tools

As you'll see in our [pyproject.toml](../pyproject.toml), we use several additional tools to help with development:

- [**ruff**](https://docs.astral.sh/ruff/): A fast Python linter
- [**isort**](https://pycqa.github.io/isort/): A tool that sorts imports in your Python code
- [**black**](https://black.readthedocs.io/en/stable/): A code formatter
- [**pyright**](https://pyright.readthedocs.io/en/stable/): A static type checker for Python
- [**pytest**](https://docs.pytest.org/en/latest/): A testing framework

These tools are configured via the `tool.ruff`, `tool.isort`, `tool.black`, `tool.pyright`, and `tool.pytest` sections in the `pyproject.toml` file.

To run these tools, you can use the `make` command. For example, to run ruff, you can run `make lint`. For more information, see the [make](../make/README.md) documentation.

