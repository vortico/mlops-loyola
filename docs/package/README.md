# MLOps Package

A production-ready ML package that demonstrates best practices for deploying machine learning models using Flama 🔥 and scikit-learn pipelines.

## Overview

This package implements a modular and scalable approach to MLOps, focusing on:
- Standardized ML pipelines using [scikit-learn](https://scikit-learn.org/stable/)
- Custom transformers for feature engineering
- Model serving through [Flama](https://flama.dev/)
- Configuration management
- Model versioning and metadata tracking

## Package Structure

This package is structured as a Python package, with the following structure:

```
mlops/
├── init.py
├── main.py # Entry point for running the API
├── app.py # Main Flama application
├── config.py # Configuration management
├── apps/ # API applications
│ └── churn/ # Churn prediction endpoint
├── pipelines/ # ML pipeline definitions
│ └── churn.py # Churn prediction pipeline
├── processors/ # Model training and inference
│ └── churn.py # Churn model processor
└── transformers/ # Custom sklearn transformers
├── feature_selector.py
└── outlier_clipper.py
```

## Key Components

### 1. ML Pipeline Architecture

The package uses scikit-learn's Pipeline API to create reproducible and maintainable ML workflows. The main components are:

- **Preprocessors**: [Standard scaling](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html), [imputation](https://scikit-learn.org/stable/modules/generated/sklearn.impute.SimpleImputer.html), and custom transformations
- **Feature Engineering**: Custom transformers for feature selection and outlier handling
- **Model Training**: [GridSearchCV](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GridSearchCV.html) for hyperparameter optimization
- **Evaluation**: Multiple metrics ([accuracy](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.accuracy_score.html), [F1](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html), [ROC-AUC](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_auc_score.html))

Example of pipeline construction:

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.feature_selection import SelectKBest
from sklearn.ensemble import RandomForestClassifier

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('imputer', SimpleImputer(strategy='mean')),
    ('feature_selector', SelectKBest(k=10)),
    ('classifier', RandomForestClassifier())
])
```

### 2. Custom Transformers

The package includes custom scikit-learn compatible transformers:

- **OutlierClipper**: Handles outliers using IQR method
- **FeatureSelector**: Selects features based on correlation threshold

### 3. Model Serving

The package uses Flama to serve models through a REST API:

- Main API at `/`
- Model-specific endpoints (e.g., `/churn/`)
- Automatic OpenAPI documentation at `/docs/`

### 4. Configuration Management

Configuration is handled through:
- YAML files for model parameters
- Environment variables for deployment settings
- Centralized config module

## Usage

To start the API, run:

```bash
python -m mlops
```


## Best Practices Demonstrated

1. **Modularity**: Each component has a single responsibility
2. **Extensibility**: Easy to add new models and transformers
3. **Reproducibility**: Pipelines ensure consistent preprocessing
4. **Configurability**: External configuration for easy deployment
5. **Monitoring**: Built-in metrics and model metadata tracking
