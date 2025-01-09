import numpy as np
import pytest

from mlops.transformers import FeatureSelector, OutlierClipper


class TestOutlierClipper:
    @pytest.mark.parametrize(
        ["data", "factor", "expected"],
        [
            pytest.param(
                np.array([[1, 10], [2, 20], [3, 30], [100, 25]]),
                1.5,
                np.array([[1, 10], [2, 20], [3, 30], [65.5, 25]]),
                id="ok_basic_clipping",
            ),
            pytest.param(
                np.array([[1, 10], [2, 20], [3, 30]]),
                1.5,
                np.array([[1, 10], [2, 20], [3, 30]]),
                id="ok_no_outliers",
            ),
            pytest.param(
                np.array([[5, 5], [5, 5], [5, 5]]),
                1.5,
                np.array([[5, 5], [5, 5], [5, 5]]),
                id="ok_all_same_values",
            ),
            pytest.param(
                np.array([[100]]),
                1.5,
                np.array([[100]]),
                id="ok_single_value",
            ),
        ],
    )
    def test_clipper_cases(self, data, factor, expected):
        clipper = OutlierClipper(factor=factor)
        result = clipper.fit_transform(data)
        np.testing.assert_allclose(result, expected, rtol=0.1)

    @pytest.mark.parametrize(
        ["input", "raises"],
        [
            pytest.param(np.array([]), pytest.raises(IndexError), id="error_empty_array"),
        ],
    )
    def test_clipper_error_cases(self, input, raises):
        clipper = OutlierClipper()
        with raises:
            clipper.fit_transform(input)


class TestFeatureSelector:
    @pytest.mark.parametrize(
        ["data", "target", "threshold", "expected"],
        [
            pytest.param(
                np.array([[1, 0, 0], [2, 0, 0], [3, 0, 0]]),
                np.array([1, 2, 3]),
                0.5,
                (3, 1),
                id="ok_perfect_correlation",
            ),
            pytest.param(
                np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]]),
                np.array([0, 1, 0]),
                0.1,
                (3, 0),
                id="ok_no_correlation",
            ),
            pytest.param(
                np.array([[1.2, 7.12, 1.43], [2, 20, 200], [3, 30, 300]]),
                np.array([0, 10, 400]),
                0.9,
                (3, 1),
                id="ok_mixed_correlations",
            ),
        ],
    )
    def test_selector_cases(self, data, target, threshold, expected):
        selector = FeatureSelector(threshold=threshold)
        result = selector.fit_transform(data, target)
        assert result.shape == expected

    @pytest.mark.parametrize(
        ["input", "target", "raises"],
        [
            pytest.param(
                np.array([["A", 1], ["B", 2]]), np.array([0, 1]), pytest.raises(TypeError), id="error_categorical_data"
            ),
        ],
    )
    def test_selector_error_cases(self, input, target, raises):
        selector = FeatureSelector()
        with raises:
            selector.fit_transform(input, target)
