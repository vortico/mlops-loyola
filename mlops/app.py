from flama import Flama, types

from mlops import apps

OPENAPI: types.OpenAPISpec = {
    "info": {
        "title": "MLOps API",
        "version": "1.0.0",
        "summary": "Serving ML API using Flama 🔥",
        "description": "Firing up with the flame",
    },
}

app = Flama(openapi=OPENAPI, docs="/docs/")


@app.get("/ping/")
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
