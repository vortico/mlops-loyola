from unittest.mock import patch

import pytest
import yaml

from mlops.config import load_model_config


class TestConfig:
    @pytest.mark.parametrize(
        ["yaml_content", "expected"],
        [
            pytest.param(
                {"model_params": {"n_estimators": 100}},
                {"model_params": {"n_estimators": 100}},
                id="ok_basic_yaml",
            ),
            pytest.param(
                {},
                {},
                id="ok_empty_yaml",
            ),
            pytest.param(
                {"data_path": "data/train.csv", "target_col": "target"},
                {"data_path": "data/train.csv", "target_col": "target"},
                id="ok_data_yaml",
            ),
        ],
    )
    def test_load_config(self, yaml_content, expected, tmp_path):
        temp_yaml = tmp_path / "model_config.yaml"
        with open(temp_yaml, "w") as f:
            yaml.dump(yaml_content, f)

        with patch("mlops.config.ROOT_PATH", tmp_path):
            result = load_model_config()
            assert result == expected

    @pytest.mark.parametrize(
        ["scenario", "raises"],
        [
            pytest.param(
                "missing_file",
                pytest.raises(FileNotFoundError),
                id="error_missing_file",
            ),
            pytest.param(
                "invalid_yaml",
                pytest.raises(yaml.YAMLError),
                id="error_invalid_yaml",
            ),
        ],
    )
    def test_load_config_errors(self, scenario, raises, tmp_path):
        temp_yaml = tmp_path / "model_config.yaml"

        if scenario == "invalid_yaml":
            with open(temp_yaml, "w") as f:
                f.write("invalid: yaml: content:\n  - : missing")

        with patch("mlops.config.ROOT_PATH", tmp_path):
            with raises:
                load_model_config()
