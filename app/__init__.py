import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask

from app.database.db_config import engine, obter_database_url
from app.database.orm_models import Base
from app.routes import register_blueprints


def create_app():
    load_dotenv(Path(__file__).resolve().parent.parent / ".env")

    # Em SQLite (desenvolvimento local) cria as tabelas automaticamente.
    # Em PostgreSQL (producao) o schema e gerenciado exclusivamente pelo Alembic.
    if obter_database_url().startswith("sqlite"):
        Base.metadata.create_all(engine)

    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY", "dev-key-troque-em-producao")
    app.config['SESSION_PERMANENT'] = True
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=8)
    register_blueprints(app)
    return app
