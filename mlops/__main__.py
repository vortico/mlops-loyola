import flama

from mlops import config
from mlops.app import app


def main():
    flama.run(flama_app=app, server_host=config.HOST, server_port=config.PORT)


if __name__ == "__main__":
    main()
