from flama import Flama

from mlops.config import CHURN_ARTIFACT_PATH

__all__ = ["app"]

app = Flama(docs=None, schema=None)

app.models.add_model(path="/", model=CHURN_ARTIFACT_PATH, name="Churn")
