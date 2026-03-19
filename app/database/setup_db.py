import sqlite3
from pathlib import Path

def criar_banco():
    diretorio_dados = Path(r"C:\Users\vinicius.gomes\Desktop\py\loja-roupa-py\dados")
    diretorio_dados.mkdir(parents=True, exist_ok=True)
    caminho_banco = diretorio_dados / "sistema_loja.db"

    try:
        conn = sqlite3.connect(caminho_banco)
        cursor = conn.cursor()

   
        cursor.execute("PRAGMA foreign_keys = ON;")

        # 1. Tabela: Clientes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE
            )
        ''')

        # 2. Tabela: Estoque
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS estoque (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_produto TEXT NOT NULL,
                tamanho TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                valor_compra REAL NOT NULL,
                UNIQUE(nome_produto, tamanho)
            )
        ''')

        # 3. Tabela: Compras
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS compras (
            id  INTEGER PRIMARY KEY AUTOINCREMENT,
            estoque_id     INTEGER NOT NULL,
            fornecedor_id  INTEGER NOT NULL,
            quantidade     TEXT    NOT NULL,
            valor_unitario REAL    NOT NULL,
            data_compra    TEXT    NOT NULL,
            FOREIGN KEY (estoque_id) REFERENCES estoque (id),
            FOREIGN KEY(fornecedor_id) REFERENCES Participantes (id))
                )
            )
        ''')

        # 4. Tabela: Vendas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vendas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER NOT NULL,
                estoque_id INTEGER NOT NULL,
                quantidade INTEGER NOT NULL,
                valor_unitario REAL NOT NULL,
                data_venda TEXT NOT NULL,
                FOREIGN KEY (cliente_id) REFERENCES clientes (id),
                FOREIGN KEY (estoque_id) REFERENCES estoque (id)
            )
        ''')

        # 5. Tabela: Contas a Pagar
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contas_a_pagar (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                compra_id INTEGER NOT NULL,
                parcela INTEGER NOT NULL,
                valor_parcela REAL NOT NULL,
                valor_pendente REAL NOT NULL,
                data_vencimento TEXT NOT NULL,
                FOREIGN KEY (compra_id) REFERENCES compras (id)
            )
        ''')

        # 6. Tabela: Contas a Receber
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contas_a_receber (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                venda_id INTEGER NOT NULL,
                parcela INTEGER NOT NULL,
                valor_parcela REAL NOT NULL,
                valor_pendente REAL NOT NULL,
                data_vencimento TEXT NOT NULL,
                FOREIGN KEY (venda_id) REFERENCES vendas (id)
            )
        ''')
        cursor.execute('''                 
            CREATE TABLE if not exists Participantes (
                id integer PRIMARY KEY  AUTOINCREMENT,
                nome TEXTO NOT NULL UNIQUE)
                       ''')

        conn.commit()
        conn.close()
        print(f"Tabelas criadas com sucesso!")
        
    except sqlite3.Error as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    criar_banco()