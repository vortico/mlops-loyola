import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

__all__ = ["OutlierClipper"]


class OutlierClipper(BaseEstimator, TransformerMixin):
    def __init__(self, factor=1.5):
        self.factor = factor
        self.lower_bounds_ = None
        self.upper_bounds_ = None

    def fit(self, X, y=None):  # type:ignore[unused-argument]
        q1 = np.percentile(X, 25, axis=0)
        q3 = np.percentile(X, 75, axis=0)
        iqr = q3 - q1
        self.lower_bounds_ = q1 - (self.factor * iqr)
        self.upper_bounds_ = q3 + (self.factor * iqr)
        return self

    def transform(self, X):
        X_clipped = np.clip(X, self.lower_bounds_, self.upper_bounds_)
        return X_clipped
