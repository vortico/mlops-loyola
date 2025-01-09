from flama import Flama

from mlops import apps

app = Flama(
    title="MLOps API",
    version="1.0.0",
    description="Serving ML/API using Flama 🔥",
    docs="/docs/",
)


@app.get("/")
def home():
    """
    tags:
        - Home
    summary:
        Returns warming message
    description:
        The function returns a hello message
    """
    return "Hello 🔥"


app.mount("/churn/", app=apps.churn, name="churn")
