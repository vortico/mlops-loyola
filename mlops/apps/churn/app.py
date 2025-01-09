from flama import Flama

from mlops.config import ROOT_PATH

__all__ = ["app"]

app = Flama(docs=None, schema=None)

app.models.add_model(
    path="/",
    model=ROOT_PATH / "artifacts" / "models" / "churn" / "model.flm",
    name="churn",
)
