import os
import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor
from pathlib import Path

class BaseRepository:
    def __init__(self):
        self.caminho_db = Path(__file__).parent.parent.parent / "dados" / "sistema_loja.db"
        self.db_url = os.environ.get("DATABASE_URL") 
        self.caminho_db.parent.mkdir(parents=True, exist_ok=True)
    
    def _get_connection(self):
        """Método privado apenas para obter a conexão correta."""
        if self.db_url:
            url_corrigida = self.db_url.replace("postgres://", "postgresql://", 1)
            return psycopg2.connect(url_corrigida, cursor_factory=RealDictCursor)
        else:
            conn = sqlite3.connect(self.caminho_db)
            conn.row_factory = sqlite3.Row
            return conn

    def executar_select(self, query, parametros=()):
        """Executa comandos de leitura (SELECT) e fecha a conexão."""
        conn = self._get_connection()
        try:
            cur = conn.cursor()
            if self.db_url:
                query = query.replace("?", "%s")
                
            cur.execute(query, parametros)
            return cur.fetchall()
        finally:
            conn.close()

    def executar_comando(self, query, parametros=()):
        """Executa comandos de escrita (INSERT, UPDATE, DELETE)."""
        conn = self._get_connection()
        try:
            with conn:
                cur = conn.cursor()
                if self.db_url:
                    query = query.replace("?", "%s")
                    
                cur.execute(query, parametros)
        finally:
            conn.close() 