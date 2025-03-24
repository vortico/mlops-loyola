from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import GridSearchCV
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

import mlops.transformers as transformers
from mlops.config import MODEL_CONFIG


class ChurnPipeline:
    def __init__(self, params, *, numeric_features, categorical_features):
        self.numeric_features = list(
            set(numeric_features).difference(MODEL_CONFIG["models"]["churn"]["drop_features"]["numerical"])
        )
        self.categorical_features = list(
            set(categorical_features).difference(MODEL_CONFIG["models"]["churn"]["drop_features"]["categorical"])
        )
        self.params = params

    def build(self):
        preprocessor = ColumnTransformer(
            [
                (
                    "numerical",
                    Pipeline(
                        [
                            ("imputer", SimpleImputer(strategy="median")),
                            ("outlier_clipper", transformers.OutlierClipper(factor=1.5)),
                            ("scaler", StandardScaler()),
                        ]
                    ),
                    self.numeric_features,
                ),
                (
                    "categorical",
                    Pipeline(
                        [
                            ("imputer", SimpleImputer(strategy="constant", fill_value="missing")),
                            ("onehot", OneHotEncoder(handle_unknown="ignore")),
                        ]
                    ),
                    self.categorical_features,
                ),
            ]
        )
        model_pipeline = Pipeline(
            [
                ("preprocessing", preprocessor),
                ("mlp_classifier", MLPClassifier(random_state=MODEL_CONFIG["models"]["churn"]["random_seed"])),
            ]
        )
        return GridSearchCV(
            model_pipeline,
            self.params,
            cv=5,
            scoring=["accuracy", "f1", "roc_auc"],
            refit="roc_auc",  # pyright: ignore
            n_jobs=-1,
        )
