import os

from dotenv import load_dotenv


load_dotenv()


def esta_no_render() -> bool:
    return bool(os.environ.get("RENDER") or os.environ.get("RENDER_SERVICE_ID"))


def obter_database_url():
    if esta_no_render():
        return os.environ.get("DATABASE_URL")

    return os.environ.get("TEST_DATABASE_URL") or os.environ.get("DATABASE_URL")


def normalizar_database_url(database_url):
    if not database_url:
        return None

    return database_url.replace("postgres://", "postgresql://", 1)
