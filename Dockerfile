FROM python:3.12

# Install poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
  ln -s /root/.local/bin/poetry /usr/local/bin/poetry

WORKDIR /app

# Copy project files
COPY mlops ./mlops/
COPY model.yaml ./
COPY pyproject.toml poetry.lock ./

# The model file should not be hard copied, as it is an artifact that can change over time.
# We should use volume mapping for that, so that the container can access the artifact stored.
# If you prefer not to use volumes, uncomment the following line (at your own risk).
# COPY artifacts ./artifacts 

# Install project dependencies using poetry
# We use --no-root to install only dependencies first
# Then install the project itself
RUN poetry config virtualenvs.create false && \
  poetry install --no-interaction --no-ansi --only main 

ENTRYPOINT ["poetry", "run", "python", "mlops/."]
CMD ["run"]
