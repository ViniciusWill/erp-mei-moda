import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

# Injetado pelos testes para sobrescrever a sessão usada pelos repositories
_override_session_factory = None


def esta_no_render() -> bool:
    return bool(os.environ.get("RENDER") or os.environ.get("RENDER_SERVICE_ID"))


def obter_database_url() -> str:
    if esta_no_render():
        url = os.environ.get("DATABASE_URL", "")
    else:
        url = os.environ.get("TEST_DATABASE_URL") or os.environ.get("DATABASE_URL") or ""

    if url:
        return url.replace("postgres://", "postgresql://", 1)

    caminho = Path(__file__).resolve().parents[2] / "dados" / "sistema_loja.db"
    caminho.parent.mkdir(parents=True, exist_ok=True)
    return f"sqlite:///{caminho}"


def _criar_engine():
    url = obter_database_url()
    if url.startswith("sqlite"):
        return create_engine(url, connect_args={"check_same_thread": False})
    return create_engine(url)


def _criar_visitor_engine():
    caminho = Path(__file__).resolve().parents[2] / "dados" / "visitante.db"
    caminho.parent.mkdir(parents=True, exist_ok=True)
    return create_engine(
        f"sqlite:///{caminho}",
        connect_args={"check_same_thread": False},
    )


engine = _criar_engine()
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

visitor_engine = _criar_visitor_engine()
VisitorSessionLocal = sessionmaker(bind=visitor_engine, autocommit=False, autoflush=False)
