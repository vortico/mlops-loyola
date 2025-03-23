from pathlib import Path

import yaml
from flama.config import Config

__all__ = [
    "MODEL_CONFIG",
    "CHURN_ARTIFACT_PATH",
    "DEBUG",
    "VERSION",
    "HOST",
    "PORT",
]

ROOT_PATH = Path(__file__).parents[1]


def load_model_config():
    with open(ROOT_PATH / "model.yaml") as f:
        config = yaml.safe_load(f)
    return config


# Model config
MODEL_CONFIG = load_model_config()
CHURN_ARTIFACT_PATH = ROOT_PATH / "artifacts" / "models" / "churn" / "model.flm"

# Flama config:
config = Config()
DEBUG = config("DEBUG", cast=bool, default=False)
VERSION = config("VERSION", cast=str, default="0.1.0")
HOST = config("HOST", default="0.0.0.0")
PORT = config("PORT", cast=int, default=8000)
