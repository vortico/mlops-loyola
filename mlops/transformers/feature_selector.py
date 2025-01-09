import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

__all__ = ["FeatureSelector"]


class FeatureSelector(BaseEstimator, TransformerMixin):
    def __init__(self, threshold=0.1):
        self.threshold = threshold
        self.selected_features_ = None

    def fit(self, X, y):
        correlations = np.array([abs(np.corrcoef(X[:, i], y)[0, 1]) for i in range(X.shape[1])])
        self.selected_features_ = correlations >= self.threshold
        return self

    def transform(self, X):
        return X[:, self.selected_features_]
