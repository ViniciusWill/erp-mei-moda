import os
import re
import sqlite3
from pathlib import Path

import psycopg2
from psycopg2.extras import RealDictCursor


class BaseRepository:
    def __init__(self):
        self.db_url = os.environ.get("DATABASE_URL")
        self.is_postgres = bool(self.db_url)

        diretorio_dados = Path(__file__).resolve().parent.parent.parent / "dados"
        diretorio_dados.mkdir(parents=True, exist_ok=True)
        self.caminho_banco = diretorio_dados / "sistema_loja.db"

    def _connect(self):
        if self.is_postgres:
            url = self.db_url.replace("postgres://", "postgresql://", 1)
            return psycopg2.connect(url, cursor_factory=RealDictCursor)

        conn = sqlite3.connect(self.caminho_banco)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def _adapt_query(self, query: str) -> str:
        if self.is_postgres:
            return query.replace("?", "%s")
        return query

    def _get_inserted_id(self, cursor, query: str):
        match = re.search(r"insert\s+into\s+([a-zA-Z_][a-zA-Z0-9_]*)", query, re.IGNORECASE)
        if not match:
            return None

        tabela = match.group(1).lower()

        if self.is_postgres:
            cursor.execute("SELECT CURRVAL(pg_get_serial_sequence(%s, 'id')) AS id", (tabela,))
            resultado = cursor.fetchone()
            return resultado["id"] if resultado else None

        cursor.execute("SELECT last_insert_rowid() AS id")
        resultado = cursor.fetchone()
        return resultado["id"] if resultado else None

    def executar_select(self, query: str, params=()):
        conn = self._connect()
        cursor = conn.cursor()
        try:
            cursor.execute(self._adapt_query(query), params)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def executar_select_um(self, query: str, params=()):
        conn = self._connect()
        cursor = conn.cursor()
        try:
            cursor.execute(self._adapt_query(query), params)
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    def executar_insert(self, query: str, params=()):
        conn = self._connect()
        cursor = conn.cursor()
        try:
            cursor.execute(self._adapt_query(query), params)
            insert_id = self._get_inserted_id(cursor, query)
            conn.commit()
            return insert_id
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()

    def executar_transacao(self, operacoes):
        conn = self._connect()
        cursor = conn.cursor()
        ids = []

        try:
            for query, params in operacoes:
                cursor.execute(self._adapt_query(query), params)

                if query.strip().lower().startswith("insert"):
                    ids.append(self._get_inserted_id(cursor, query))

            conn.commit()
            return ids
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()
