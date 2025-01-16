FROM python:3.12-slim

RUN apt-get update && apt-get -y upgrade \
  && pip install --upgrade pip \
  && pip --version

RUN apt-get update && apt-get install -y procps \
  && rm -rf /var/lib/apt/lists/*

RUN pip install mlflow

# Create directories and set permissions
RUN mkdir -p /mlflow/artifacts /mlflow/mlruns && \
  chown -R 50000:0 /mlflow && \
  chmod -R 777 /mlflow

# Set working directory
WORKDIR /mlflow

# Expose MLflow's default port
EXPOSE 5001

# Run MLflow server
# --host 0.0.0.0 allows external connections
# --backend-store-uri specifies where to store run metadata
# --default-artifact-root specifies where to store artifacts
CMD mlflow server \
  --host 0.0.0.0 \
  --port 5001 \
  --backend-store-uri sqlite:///mlflow.db \
  --default-artifact-root /mlflow/artifacts
