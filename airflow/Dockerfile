FROM apache/airflow:2.10.4

USER root
# Install poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
  ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Copy project files
COPY mlops ./mlops/
COPY model_config.yaml ./
COPY pyproject.toml poetry.lock ./

# Install project dependencies using poetry
# We use --no-root to install only dependencies first
# Then install the project itself
RUN poetry config virtualenvs.create false && \
  poetry install --no-interaction --no-ansi --only main && \
  poetry install --no-interaction --no-ansi --only airflow && \
  poetry install --no-interaction --no-ansi --only-root

# Switch to airflow user
USER airflow

