import os
import sqlite3
import psycopg2
from pathlib import Path

def criar_banco():

    db_url = os.environ.get("DATABASE_URL")

    # Configurações para SQLite 
    diretorio_dados = Path(__file__).parent.parent.parent / "dados"
    diretorio_dados.mkdir(parents=True, exist_ok=True)
    caminho_banco = diretorio_dados / "sistema_loja.db"

    # --- LÓGICA DE CONEXÃO E SINTAXE ---
    if db_url:
        print("Conectando ao PostgreSQL (Render)...")
        url_corrigida = db_url.replace("postgres://", "postgresql://", 1)
        conn = psycopg2.connect(url_corrigida)
        id_type = "SERIAL PRIMARY KEY" 
    else:
        print("Conectando ao SQLite (Local)...")
        conn = sqlite3.connect(caminho_banco)
        id_type = "INTEGER PRIMARY KEY AUTOINCREMENT"

    try:
        cursor = conn.cursor()

        # Pragma só existe no SQLite
        if not db_url:
            cursor.execute("PRAGMA foreign_keys = ON;")

        # 1. Tabela: Clientes
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS clientes (
                id {id_type},
                nome TEXT NOT NULL UNIQUE
            )
        ''')

        # 2. Tabela: Estoque
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS estoque (
                id {id_type},
                nome_produto TEXT NOT NULL,
                tamanho TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                valor_compra REAL NOT NULL,
                UNIQUE(nome_produto, tamanho)
            )
        ''')

        # 3. Tabela: Participantes 
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS Participantes (
                id {id_type},
                nome TEXT NOT NULL UNIQUE
            )
        ''')

        # 4. Tabela: Compras 
        cursor.execute(f'''
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
        ''')

        # 5. Tabela: Vendas
        cursor.execute(f'''
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
        ''')

        # 6. Tabela: Contas a Pagar
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS contas_a_pagar (
                id {id_type},
                compra_id INTEGER NOT NULL,
                parcela INTEGER NOT NULL,
                valor_parcela REAL NOT NULL,
                valor_pendente REAL NOT NULL,
                data_vencimento TEXT NOT NULL,
                FOREIGN KEY (compra_id) REFERENCES compras (id)
            )
        ''')

        # 7. Tabela: Contas a Receber
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS contas_a_receber (
                id {id_type},
                venda_id INTEGER NOT NULL,
                parcela INTEGER NOT NULL,
                valor_parcela REAL NOT NULL,
                valor_pendente REAL NOT NULL,
                data_vencimento TEXT NOT NULL,
                FOREIGN KEY (venda_id) REFERENCES vendas (id)
            )
        ''')

        conn.commit()
        print("Tabelas criadas com sucesso!")
        
    except Exception as e:
        conn.rollback() 
        print(f"Erro ao criar tabelas: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    criar_banco()