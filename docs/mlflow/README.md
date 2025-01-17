# MLflow Integration

This section covers the MLflow setup and integration for our MLOps pipeline, providing experiment tracking, model registry, and artifact storage capabilities.

## Overview

The setup includes:
- Containerized MLflow server using Docker
- SQLite backend for experiment tracking
- Local artifact storage
- REST API access for remote tracking

## Configuration Details

### Docker Setup
The MLflow server runs in a containerized environment with:
- Python 3.12 slim base image
- SQLite backend database
- Local artifact storage
- Port 5001 exposed for web UI and API access

### Storage Configuration
- **Backend Store**: SQLite database (`mlflow.db`)
- **Artifact Store**: Local directory (`/mlflow/artifacts`)
- **Run History**: Stored in `/mlflow/mlruns`

### Security
- Default user permissions set to UID 50000
- Directory permissions set to 777 for artifact storage
- No authentication enabled by default (suitable for local development)

## Usage

### Tracking Experiments

To track experiments, you can use the MLflow Python API or the REST API.

### Example: Python API

```python
import mlflow

mlflow.set_tracking_uri('http://localhost:5001')
mlflow.set_experiment('my_experiment')

# Start a new run
with mlflow.start_run():
    mlflow.log_param('param1', 'value1')
    mlflow.log_metric('metric1', 1.0)
```

## Integration Points

### With Training Pipeline
- Log hyperparameters before training
- Track metrics during training
- Store model artifacts after training
- Register successful models

### With Airflow
- DAGs can access MLflow tracking server
- Automated model registration
- Pipeline metadata logging

### With Deployment
- Load models from registry
- Access model versions
- Track model serving metrics

## Best Practices

1. **Experiment Organization**
   - Use meaningful experiment names
   - Group related runs under the same experiment
   - Tag runs appropriately

2. **Artifact Management**
   - Clean up unnecessary artifacts regularly
   - Use consistent naming conventions
   - Version models appropriately

3. **Metric Tracking**
   - Log all relevant metrics
   - Include validation metrics
   - Track resource usage when possible

4. **Model Registry**
   - Use semantic versioning
   - Document model transitions
   - Maintain clear staging/production separation

## Troubleshooting

Common issues and solutions:

1. **Connection Issues**
   - Verify the MLflow server is running: `docker ps`
   - Check the tracking URI is correct
   - Ensure port 5001 is accessible

2. **Storage Problems**
   - Check disk space for artifacts
   - Verify database permissions
   - Monitor SQLite database size

3. **Performance Issues**
   - Consider cleaning old runs
   - Archive unused artifacts
   - Monitor server resources

## Additional Resources

- [MLflow Documentation](https://www.mlflow.org/docs/latest/index.html)
- [MLflow API Reference](https://www.mlflow.org/docs/latest/python_api/index.html)
- [MLflow Model Registry](https://www.mlflow.org/docs/latest/model-registry.html)
- [Docker Documentation](https://docs.docker.com/)