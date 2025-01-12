# Customer Churn Prediction MLOps Project

## Overview
This project focuses on predicting customer churn for a subscription-based service. The goal is to identify customers who are likely to discontinue their service, allowing the business to take proactive measures to retain them. The project requires implementing a complete MLOps pipeline including data preprocessing, model training, and deployment.

## Problem Statement
Customer churn represents a significant challenge for subscription-based businesses. Early identification of customers likely to churn enables targeted retention efforts. The data science team needs to develop a robust, production-ready machine learning pipeline that can process customer data and provide accurate churn predictions.

## Dataset Description
The dataset contains historical customer information. The data is expected to be provided in `.parquet` format, with consistent column names and data types. Each row represents a unique customer record with their associated features and churn status.

## Technical Requirements

### Data Preprocessing
The pipeline should handle:
- Missing value imputation (median for numerical, 'missing' for categorical)
  - Implement robust handling of missing values to ensure pipeline stability
  - Maintain separate statistics for training and inference
- Outlier treatment using IQR method (factor=1.5)
  - Identify and handle outliers in numerical features
  - Document outlier thresholds for monitoring
- Feature scaling ([StandardScaler](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html)) for numerical features
  - Scale features to zero mean and unit variance
  - Store scaling parameters for inference
- Categorical encoding ([OneHotEncoder](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OneHotEncoder.html)) with unknown category handling
  - Handle new categories during inference
  - Implement dimension reduction if needed

### Model Architecture
- Neural Network (MLPClassifier) with GridSearchCV optimization
  - Define architecture search space including layers and neurons
  - Implement early stopping to prevent overfitting
- Cross-validation (k=5)
  - Ensure stratified splitting for balanced class distribution
  - Maintain consistent validation strategy
- Performance metrics:
  - ROC-AUC (primary metric for model selection)
  - Accuracy
  - F1 Score
  - Include confidence intervals for all metrics

### MLOps Pipeline Requirements
1. Modular code structure:
   - Separate transformer classes for custom preprocessing
     - Each transformer should follow sklearn's transformer interface
     - Include proper error handling and validation
   - Pipeline class for model assembly
     - Ensure reproducibility of the entire pipeline
     - Include validation steps between components
   - Processor class for training and inference
     - Handle both batch and single-instance predictions
     - Include input validation and error handling

2. Model versioning and metadata:
   - Model ID (UUID)
     - Unique identifier for each trained model
     - Link to training data version
   - Timestamp
   - Training parameters
   - Performance metrics
   - Author information
   - Model description and version
     - Include dependencies and environment specifications
     - Document any data preprocessing decisions

3. Configuration management:
   - Hyperparameter grids
     - Define search spaces for model optimization
     - Include validation ranges for parameters
   - Feature lists
     - Maintain separate lists for numerical and categorical features
     - Document feature engineering steps
   - Random seed
   - Test size
   - Model metadata
     - Store all configuration in version-controlled YAML files
     - Include validation schemas for configurations

4. Model Serving:
   - REST API implementation (e.g., using [Flama](https://flama.dev/))
     - Define clear API contracts and documentation
     - Include request/response validation
   - Endpoint for real-time predictions
     - Implement proper error handling
     - Include input validation and sanitization
   - Input validation
   - Error handling and response formatting
     - Provide meaningful error messages
     - Include proper HTTP status codes
   - API documentation
     - OpenAPI/Swagger documentation
     - Include example requests and responses

5. Experiment Tracking:
   - [MLflow](https://mlflow.org/) integration for experiment tracking
     - Track all experiments with unique identifiers
     - Store environment information
   - Logging of:
     - Model parameters
     - Evaluation metrics
     - Model artifacts
     - Training metadata
     - Data versioning
       - Include data snapshots or references
       - Track feature engineering steps
   - Experiment comparison and visualization
     - Provide tools for comparing different runs
     - Include performance visualization

6. Pipeline Orchestration:
   - [Airflow](https://airflow.apache.org/) DAGs for workflow automation
     - Define clear dependencies between tasks
     - Include proper error handling and retries
   - Pipeline steps:
     - Data validation
     - Model training
     - Model evaluation
     - Model deployment
       - Include rollback capabilities
       - Implement blue-green deployment
   - Scheduling and monitoring
     - Define retraining schedules
     - Monitor pipeline health
   - Error handling and notifications
     - Alert on pipeline failures
     - Implement proper logging
   - Pipeline versioning
     - Track changes in pipeline configuration
     - Include documentation for each version

## Expected Deliverables
1. Preprocessing transformers
   - Well-documented custom transformer classes
   - Unit tests for each transformer
2. Model pipeline implementation
   - Complete sklearn-compatible pipeline
   - Documentation of pipeline steps
3. Training and inference processor
   - Separate modules for training and inference
   - Performance optimization for inference
4. Configuration files
   - YAML files with validation schemas
   - Documentation of all parameters
5. Documentation
   - API documentation
   - Development setup guide
   - Deployment instructions
6. Unit tests
   - Coverage for all critical components
   - Integration tests for the pipeline

## Performance Targets
- Minimum ROC-AUC score: 0.80
  - Measured on hold-out test set
  - Include confidence intervals
- Maximum training time: 10 minutes
  - Including hyperparameter optimization
  - Measured on specified hardware
- Model size: < 100MB
  - Including all required artifacts
  - Compressed format for deployment
- Inference time: < 100ms per prediction
  - Measured at p95 latency
  - Under specified load conditions

## Deployment Considerations
- Model serialization using [Flama](https://flama.dev/)
  - Include version compatibility checks
  - Implement proper error handling
- REST API deployment with health checks
  - Monitor API performance and availability
  - Include resource utilization metrics
- [MLflow](https://mlflow.org/) server setup for experiment tracking
  - Configure proper authentication
  - Implement backup procedures
- [Airflow](https://airflow.apache.org/) deployment for pipeline orchestration
  - Set up proper scheduling
  - Monitor DAG performance
- Reproducible training pipeline
  - Document all dependencies
  - Include environment setup scripts
- Logging and monitoring capabilities
  - Implement structured logging
  - Set up alerting thresholds
- Error handling and validation
  - Define error handling strategies
  - Implement input validation
- CI/CD integration
  - Include automated testing
  - Implement deployment automation

## Infrastructure Requirements
1. [MLflow](https://mlflow.org/) tracking server
   - Scalable storage for artifacts
   - Backup and recovery procedures
2. [Airflow](https://airflow.apache.org/) deployment
   - Proper resource allocation
   - Monitoring and alerting setup
3. API hosting environment
   - Load balancing configuration
   - Auto-scaling capabilities
4. Artifact storage
   - Version control for models
   - Backup procedures
5. Monitoring system
   - Performance metrics collection
   - Alert configuration
