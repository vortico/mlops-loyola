# Airflow Integration

This section covers the Apache Airflow integration for our MLOps pipeline, which handles workflow orchestration and scheduling of our machine learning tasks.

## Overview

The setup includes:
- A customized Airflow installation using Docker
- Integration with MLflow for model tracking
- Example DAGs for demonstration and production use
- Complete pipeline for model training and evaluation

## Project Structure

This section covers the Apache Airflow integration for our MLOps pipeline, which handles workflow orchestration and scheduling of our machine learning tasks. The folder structure is as follows:

```bash
airflow/
├── Dockerfile # Custom Airflow image configuration
├── docker-compose.yaml # Docker services orchestration
└── dags/
├── example.py # Simple example DAG
└── train_pipeline.py # Production training pipeline DAG
```


## Setup Instructions

1. Build the custom Airflow image:

```bash
docker build -t airflow-mlops:latest -f airflow/Dockerfile .
```

This is not actually needed if you use the makefile command.

2. Start the Airflow services:

```bash
docker compose -f airflow/docker-compose.yaml up
```

or simply run the makefile command:

```bash
make serve-airflow
```
3. Access the Airflow UI at `http://localhost:8080` with:
- Username: airflow
- Password: airflow

## Available DAGs

### 1. Simple Example DAG
- **File**: `dags/example.py`
- **Purpose**: Demonstrates basic Airflow concepts
- **Schedule**: Daily
- **Tasks**: 4 simple Python tasks showing task dependencies

### 2. Training Pipeline DAG
- **File**: `dags/train_pipeline.py`
- **Purpose**: Production ML training pipeline
- **Schedule**: Weekly
- **Tasks**:
  - Load and split data
  - Train model
  - Evaluate model
  - Register model in MLflow
  - Load and test model

## Key Components

### Custom Dockerfile
- Based on `apache/airflow:2.10.4`
- Includes Poetry for dependency management
- Installs project dependencies and MLOps package

### Docker Compose Configuration
- Includes standard Airflow services (webserver, scheduler, worker)
- Integrates MLflow service
- Mounts necessary volumes for data and artifacts
- Sets up networking between services

### Volume Mounts
- `./dags`: Airflow DAG files
- `../data`: Training data
- `../artifacts`: Model artifacts
- `../mlflow/data`: MLflow tracking data

## Usage

1. Place your training data in the `data/` directory
2. DAGs will automatically be picked up from the `dags/` directory
3. Models and artifacts are stored in `artifacts/`
4. MLflow tracking server is available at `http://localhost:5001`

## Best Practices

1. Always test DAGs with `airflow dags test [dag_id] [execution_date]`
2. Use XCom sparingly and only for small data transfers
3. Keep tasks atomic and idempotent
4. Monitor task duration and memory usage
5. Use appropriate retry configurations for production DAGs

## Troubleshooting

Common issues and solutions:

1. **Permission Issues**
   - Ensure AIRFLOW_UID is set correctly in your environment
   - Check volume mount permissions

2. **Connection Errors**
   - Verify all services are healthy using `docker-compose ps`
   - Check network connectivity between services

3. **MLflow Integration Issues**
   - Confirm MLflow service is running
   - Verify MLflow tracking URI is correctly set

## Additional Resources

- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [MLflow Documentation](https://www.mlflow.org/docs/latest/index.html)
- [Docker Compose Documentation](https://docs.docker.com/compose/)