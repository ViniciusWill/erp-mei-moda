import argparse
import os
import sys
from pathlib import Path
from urllib.parse import urlparse

import psycopg2
from dotenv import load_dotenv
from psycopg2 import sql

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

from app.database.db_config import normalizar_database_url
from app.database.setup_db import criar_banco


TABLES = [
    "clientes",
    "estoque",
    "participantes",
    "compras",
    "vendas",
    "contas_a_pagar",
    "contas_a_receber",
]


def mascarar_url(database_url: str) -> str:
    parsed = urlparse(database_url)
    usuario = parsed.username or ""
    host = parsed.hostname or ""
    porta = f":{parsed.port}" if parsed.port else ""
    banco = parsed.path.lstrip("/")
    return f"{parsed.scheme}://{usuario}:***@{host}{porta}/{banco}"


def obter_urls():
    load_dotenv(ROOT_DIR / ".env")

    prod_url = os.environ.get("PROD_DATABASE_URL") or os.environ.get("PRODUCTION_DATABASE_URL")
    test_url = os.environ.get("TEST_DATABASE_URL")

    if not prod_url:
        raise RuntimeError("Defina PROD_DATABASE_URL no seu .env local.")

    if not test_url:
        raise RuntimeError("Defina TEST_DATABASE_URL no seu .env local.")

    prod_url = normalizar_database_url(prod_url)
    test_url = normalizar_database_url(test_url)

    if prod_url == test_url:
        raise RuntimeError("PROD_DATABASE_URL e TEST_DATABASE_URL nao podem ser iguais.")

    if os.environ.get("RENDER") or os.environ.get("RENDER_SERVICE_ID"):
        raise RuntimeError("Este script foi feito apenas para rodar localmente, nunca no Render.")

    return prod_url, test_url


def confirmar(prod_url: str, test_url: str, yes: bool):
    if yes:
        return

    print("Este script vai apagar e recriar os dados do banco de TESTE.")
    print(f"Origem:  {mascarar_url(prod_url)}")
    print(f"Destino: {mascarar_url(test_url)}")
    resposta = input("Digite COPIAR para continuar: ").strip().upper()

    if resposta != "COPIAR":
        raise RuntimeError("Operacao cancelada.")


def buscar_linhas(conn, tabela: str):
    with conn.cursor() as cursor:
        cursor.execute(
            sql.SQL("SELECT * FROM {} ORDER BY id").format(sql.Identifier(tabela))
        )
        colunas = [coluna[0] for coluna in cursor.description]
        linhas = cursor.fetchall()

    return colunas, linhas


def limpar_destino(conn):
    with conn.cursor() as cursor:
        tabelas = sql.SQL(", ").join(sql.Identifier(tabela) for tabela in TABLES)
        cursor.execute(
            sql.SQL("TRUNCATE TABLE {} RESTART IDENTITY CASCADE").format(tabelas)
        )
    conn.commit()


def inserir_linhas(conn, tabela: str, colunas, linhas):
    if not linhas:
        return 0

    campos = sql.SQL(", ").join(sql.Identifier(coluna) for coluna in colunas)
    placeholders = sql.SQL(", ").join(sql.Placeholder() for _ in colunas)

    query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
        sql.Identifier(tabela),
        campos,
        placeholders,
    )

    with conn.cursor() as cursor:
        cursor.executemany(query, linhas)

    return len(linhas)


def ajustar_sequence(conn, tabela: str):
    with conn.cursor() as cursor:
        cursor.execute("SELECT pg_get_serial_sequence(%s, 'id')", (tabela,))
        sequence = cursor.fetchone()[0]

        if not sequence:
            return

        cursor.execute(
            sql.SQL("SELECT COALESCE(MAX(id), 0) FROM {}").format(sql.Identifier(tabela))
        )
        maior_id = cursor.fetchone()[0]

        if maior_id:
            cursor.execute("SELECT setval(%s, %s, true)", (sequence, maior_id))
        else:
            cursor.execute("SELECT setval(%s, 1, false)", (sequence,))


def sincronizar(prod_url: str, test_url: str):
    os.environ["TEST_DATABASE_URL"] = test_url
    criar_banco()

    origem = psycopg2.connect(prod_url)
    destino = psycopg2.connect(test_url)

    try:
        limpar_destino(destino)

        totais = {}
        for tabela in TABLES:
            colunas, linhas = buscar_linhas(origem, tabela)
            totais[tabela] = inserir_linhas(destino, tabela, colunas, linhas)
            ajustar_sequence(destino, tabela)

        destino.commit()
        return totais
    except Exception:
        destino.rollback()
        raise
    finally:
        origem.close()
        destino.close()


def main():
    parser = argparse.ArgumentParser(
        description="Replica os dados do PostgreSQL de producao para o PostgreSQL de teste."
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="Executa sem pedir confirmacao interativa.",
    )
    args = parser.parse_args()

    prod_url, test_url = obter_urls()
    confirmar(prod_url, test_url, args.yes)
    totais = sincronizar(prod_url, test_url)

    print("Banco de teste sincronizado com sucesso.")
    for tabela, total in totais.items():
        print(f"- {tabela}: {total} registro(s)")


if __name__ == "__main__":
    main()
