from flask import Flask

from app.routes import register_blueprints


def create_app():
    app = Flask(__name__)
    app.secret_key = "loja-roupa-key"

    register_blueprints(app)

    return app
