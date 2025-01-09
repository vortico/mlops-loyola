import datetime
import logging
import typing as t
import uuid
from pathlib import Path

import flama
import numpy as np
import pandas as pd
from sklearn.metrics import f1_score, roc_auc_score
from sklearn.model_selection import train_test_split

import mlops.pipelines as pipelines
from mlops.config import MODEL_CONFIG

logger = logging.getLogger(__name__)

__all__ = ["ChurnProcessor"]


class ChurnProcessor:
    def __init__(self, config=MODEL_CONFIG):
        self.config = config["models"]["churn"]
        self._pipeline = None

    @property
    def pipeline(self):
        if self._pipeline is None:
            raise ValueError(
                "This ChurnModel instance is not fitted yet. Call 'train' with "
                "appropriate arguments before using this estimator."
            )
        return self._pipeline

    def compute_metrics(self, X, y):
        y_pred = self.pipeline.predict(X)

        return {
            "accuracy": self.pipeline.score(X, y),
            "roc_auc_score": roc_auc_score(y, y_pred),
            "f1_score": f1_score(y, y_pred),
        }

    def train(self, X, y):
        logger.info("Training process")

        numeric_features = [
            X.columns.get_loc(c)
            for c in X.select_dtypes(include=["int64", "float64"])
            .drop(self.config["drop_features"]["numerical"], axis=1)
            .columns.values
        ]

        categorical_features = [
            X.columns.get_loc(c)
            for c in X.select_dtypes(include=["object"])
            .drop(self.config["drop_features"]["categorical"], axis=1)
            .columns.values
        ]

        self._pipeline = pipelines.ChurnPipeline(
            self.config["param_grid"], numeric_features=numeric_features, categorical_features=categorical_features
        ).build()

        self._pipeline.fit(X, y)

        return self

    def dump(self, metrics, model_path="models/trained_model.flm"):
        logger.info("Saving model to %s", model_path)
        flama.dump(
            self.pipeline,
            model_path,
            model_id=uuid.uuid4(),
            timestamp=datetime.datetime.now(),
            params=self.pipeline.best_params_,
            metrics=metrics,
            extra={
                "model_author": self.config.get("author", "Unknown"),
                "model_description": self.config.get("description", "ML Model"),
                "model_version": self.config.get("version", "1.0.0"),
                "tags": self.config.get("tags", []),
            },
        )
        return self

    @classmethod
    def load(cls, model_path="models/trained_model.flm") -> t.Self:
        logger.info("Loading model from %s", model_path)
        pipeline = flama.load(model_path)

        obj = cls()
        obj._pipeline = pipeline.model
        return obj

    def predict(self, X: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
        predictions = self.pipeline.predict(X)  # This will raise error if pipeline is not fitted
        probabilities = self.pipeline.predict_proba(X)

        logger.info("Predictions completed for %s samples", len(predictions))
        return predictions, probabilities


if __name__ == "__main__":
    try:
        # Training example
        logger.info("Starting model training pipeline")
        data_path = Path(__file__).parent.parent / "data" / "churn" / "data.parquet"
        dataset = pd.read_parquet(data_path)

        X = dataset.drop(columns=[MODEL_CONFIG["models"]["churn"]["target"]])
        y = dataset[MODEL_CONFIG["models"]["churn"]["target"]]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=MODEL_CONFIG["models"]["churn"]["test_size"]
        )

        pipeline = ChurnProcessor().train(X_train, y_train)
        predictions, probabilities = pipeline.predict(X_test)  # pyright: ignore

        metrics = pipeline.compute_metrics(X_test, y_test)
        pipeline.dump(metrics=metrics, model_path=(data_path.parent / "model.flm").as_posix())

        # Create results DataFrame
        results = pd.DataFrame(
            {"prediction": predictions, "probability": probabilities[:, 1]}  # Probability of positive class
        )
        logger.info("Prediction results:\n%s", results.head())

    except Exception as e:
        logger.exception("An error occurred: %s", str(e))
