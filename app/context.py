import docker
import yaml

from flask_sqlalchemy import SQLAlchemy

db = None
dclient = None


def init(app):
    global db
    global dclient

    with open("config.yml", 'r') as f:
        try:
            app.config.update(yaml.safe_load(f))
        except yaml.YAMLError as exc:
            print(exc)

    # The SQLite URI is defined in the Flask's config file
    db = SQLAlchemy(app)

    dclient = docker.from_env()
