from contextlib import nullcontext as does_not_raise

import pytest
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline

from mlops.pipelines.churn import ChurnPipeline


class TestChurnPipeline:
    @pytest.fixture
    def basic_features(self):
        return {"numeric": ["age", "salary"], "categorical": ["state", "gender"]}

    @pytest.fixture
    def basic_params(self):
        return {"mlp_classifier__hidden_layer_sizes": [(10,), (20,)]}

    @pytest.mark.parametrize(
        ["params", "numeric_features", "categorical_features", "expected_attributes"],
        [
            pytest.param(
                {"mlp_classifier__hidden_layer_sizes": [(10,)]},
                ["age", "salary"],
                ["state", "gender"],
                {
                    "params": {"mlp_classifier__hidden_layer_sizes": [(10,)]},
                    "numeric_features": ["age", "salary"],
                    "categorical_features": ["state", "gender"],
                },
                id="ok_basic_features",
            ),
            pytest.param(
                {"mlp_classifier__hidden_layer_sizes": [(5,)]},
                [],
                ["category1"],
                {
                    "params": {"mlp_classifier__hidden_layer_sizes": [(5,)]},
                    "numeric_features": [],
                    "categorical_features": ["category1"],
                },
                id="ok_only_categorical",
            ),
            pytest.param(
                {"mlp_classifier__hidden_layer_sizes": [(15,)]},
                ["numeric1"],
                [],
                {
                    "params": {"mlp_classifier__hidden_layer_sizes": [(15,)]},
                    "numeric_features": ["numeric1"],
                    "categorical_features": [],
                },
                id="ok_only_numeric",
            ),
        ],
    )
    def test_initialization(self, params, numeric_features, categorical_features, expected_attributes):
        pipeline = ChurnPipeline(params, numeric_features=numeric_features, categorical_features=categorical_features)
        assert set(pipeline.params) == set(expected_attributes["params"])
        assert set(pipeline.numeric_features) == set(expected_attributes["numeric_features"])
        assert set(pipeline.categorical_features) == set(expected_attributes["categorical_features"])

    def test_build_pipeline_structure(self, basic_features, basic_params):
        pipeline = ChurnPipeline(
            basic_params, numeric_features=basic_features["numeric"], categorical_features=basic_features["categorical"]
        )

        model = pipeline.build()

        assert isinstance(model, GridSearchCV)
        assert isinstance(model.estimator, Pipeline)
        assert len(model.estimator.steps) == 2
        assert model.estimator.steps[0][0] == "preprocessing"
        assert model.estimator.steps[1][0] == "mlp_classifier"
        assert model.scoring == ["accuracy", "f1", "roc_auc"]
        assert model.refit == "roc_auc"
        assert model.cv == 5
        assert model.n_jobs == -1
        assert model.param_grid == basic_params

    @pytest.mark.parametrize(
        ["params", "raises"],
        [
            pytest.param({}, does_not_raise(), id="ok_empty_param_grid"),
            pytest.param({"invalid_param": [1, 2]}, does_not_raise(), id="ok_invalid_param_name"),
        ],
    )
    def test_build(self, basic_features, params, raises):
        pipeline = ChurnPipeline(
            params, numeric_features=basic_features["numeric"], categorical_features=basic_features["categorical"]
        )
        with raises:
            pipeline.build()
