import sqlite3
import sys
from pathlib import Path

import psycopg2

if __package__ in (None, ""):
    sys.path.append(str(Path(__file__).resolve().parents[2]))

from app.database.db_config import normalizar_database_url, obter_database_url


def garantir_coluna(conn, db_url, tabela: str, coluna: str, definicao: str):
    cursor = conn.cursor()
    try:
        if db_url:
            cursor.execute(
                """
                SELECT 1
                FROM information_schema.columns
                WHERE table_name = %s
                  AND column_name = %s
                """,
                (tabela.lower(), coluna.lower()),
            )
            if not cursor.fetchone():
                cursor.execute(f'ALTER TABLE "{tabela}" ADD COLUMN "{coluna}" {definicao}')
        else:
            cursor.execute(f"PRAGMA table_info({tabela})")
            colunas = [row[1].lower() for row in cursor.fetchall()]
            if coluna.lower() not in colunas:
                cursor.execute(f'ALTER TABLE {tabela} ADD COLUMN {coluna} {definicao}')
        conn.commit()
    finally:
        cursor.close()


def criar_banco():
    db_url = obter_database_url()

    diretorio_dados = Path(__file__).parent.parent.parent / "dados"
    diretorio_dados.mkdir(parents=True, exist_ok=True)
    caminho_banco = diretorio_dados / "sistema_loja.db"

    if db_url:
        print("Conectando ao PostgreSQL...")
        url_corrigida = normalizar_database_url(db_url)
        conn = psycopg2.connect(url_corrigida)
        id_type = "SERIAL PRIMARY KEY"
    else:
        print("Conectando ao SQLite (Local)...")
        conn = sqlite3.connect(caminho_banco)
        id_type = "INTEGER PRIMARY KEY AUTOINCREMENT"

    try:
        cursor = conn.cursor()

        if not db_url:
            cursor.execute("PRAGMA foreign_keys = ON;")

        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS clientes (
                id {id_type},
                nome TEXT NOT NULL UNIQUE,
                cpf VARCHAR(11)
            )
            """
        )

        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS estoque (
                id {id_type},
                nome_produto TEXT NOT NULL,
                tamanho TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                valor_compra REAL NOT NULL,
                UNIQUE(nome_produto, tamanho)
            )
            """
        )

        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS Participantes (
                id {id_type},
                nome TEXT NOT NULL UNIQUE,
                Cnpj VARCHAR(14)
            )
            """
        )

        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS compras (
                id {id_type},
                estoque_id INTEGER NOT NULL,
                fornecedor_id INTEGER NOT NULL,
                quantidade INTEGER NOT NULL,
                valor_unitario REAL NOT NULL,
                data_compra TEXT NOT NULL,
                FOREIGN KEY (estoque_id) REFERENCES estoque (id),
                FOREIGN KEY (fornecedor_id) REFERENCES Participantes (id)
            )
            """
        )

        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS vendas (
                id {id_type},
                cliente_id INTEGER NOT NULL,
                estoque_id INTEGER NOT NULL,
                quantidade INTEGER NOT NULL,
                valor_unitario REAL NOT NULL,
                data_venda TEXT NOT NULL,
                FOREIGN KEY (cliente_id) REFERENCES clientes (id),
                FOREIGN KEY (estoque_id) REFERENCES estoque (id)
            )
            """
        )

        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS contas_a_pagar (
                id {id_type},
                compra_id INTEGER NOT NULL,
                parcela INTEGER NOT NULL,
                valor_parcela REAL NOT NULL,
                valor_pendente REAL NOT NULL,
                data_vencimento TEXT NOT NULL,
                FOREIGN KEY (compra_id) REFERENCES compras (id)
            )
            """
        )

        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS contas_a_receber (
                id {id_type},
                venda_id INTEGER NOT NULL,
                parcela INTEGER NOT NULL,
                valor_parcela REAL NOT NULL,
                valor_pendente REAL NOT NULL,
                data_vencimento TEXT NOT NULL,
                FOREIGN KEY (venda_id) REFERENCES vendas (id)
            )
            """
        )

        conn.commit()
        garantir_coluna(conn, db_url, "clientes", "cpf", "VARCHAR(11)")
        garantir_coluna(conn, db_url, "Participantes", "Cnpj", "VARCHAR(14)")
        print("Tabelas criadas com sucesso!")

    except Exception as e:
        conn.rollback()
        print(f"Erro ao criar tabelas: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    criar_banco()
