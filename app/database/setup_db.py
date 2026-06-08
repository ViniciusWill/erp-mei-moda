"""
setup_db.py — mantido por compatibilidade com start commands antigos.

A partir da v2.0 o schema e gerenciado pelo Alembic.
Este script apenas executa 'alembic upgrade head' e encerra.

Start command recomendado (Render):
    alembic upgrade head && gunicorn run:app
"""
import subprocess
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))


def criar_banco():
    print("setup_db.py: delegando para 'alembic upgrade head'...")
    resultado = subprocess.run(
        [sys.executable, "-m", "alembic", "upgrade", "head"],
        cwd=str(Path(__file__).resolve().parents[2]),
    )
    if resultado.returncode != 0:
        print("Erro ao executar alembic upgrade head.")
        sys.exit(resultado.returncode)
    print("Migrations aplicadas com sucesso.")


if __name__ == "__main__":
    criar_banco()
