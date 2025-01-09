from pathlib import Path

import yaml
from flama.config import Config

__all__ = ["ROOT_PATH", "MODEL_CONFIG", "DEBUG", "VERSION", "HOST", "PORT"]


ROOT_PATH = Path(__file__).parent.parent


def load_model_config():
    with open(ROOT_PATH / "model_config.yaml") as f:
        config = yaml.safe_load(f)
    return config


MODEL_CONFIG = load_model_config()

# Flama config:
config = Config()
DEBUG = config("DEBUG", cast=bool, default=False)
VERSION = config("VERSION", cast=str, default="0.1.0")
HOST = config("HOST", default="0.0.0.0")
PORT = config("PORT", default=8000)
