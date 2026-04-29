from flask import Flask
from app.database.setup_db import criar_banco
from app.routes import register_blueprints


def create_app():
    criar_banco()
    app = Flask(__name__)
    app.secret_key = "loja-roupa-key"

    register_blueprints(app)


    return app
