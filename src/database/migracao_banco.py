import sqlite3
import pandas as pd
from pathlib import Path


def executar_migracao():
    # 1. Definir os caminhos
    BASE_DIR = Path(r"C:\Users\vinicius.gomes\Desktop\py\loja-roupa-py")
    ARQUIVO_EXCEL = BASE_DIR / "dados" / "Controle.xlsx"
    CAMINHO_BANCO = BASE_DIR / "dados" / "sistema_loja.db"

    print(f"A ler dados do Excel em: {ARQUIVO_EXCEL}...")
    
    try:
        # Carrega as abas do Excel
        df_clientes = pd.read_excel(ARQUIVO_EXCEL, sheet_name="Clientes")
        df_estoque = pd.read_excel(ARQUIVO_EXCEL, sheet_name="Estoque")
        df_vendas = pd.read_excel(ARQUIVO_EXCEL, sheet_name="Vendas")
        df_compras = pd.read_excel(ARQUIVO_EXCEL, sheet_name="Compras")
    except Exception as e:
        print(f"ERRO: Não foi possível ler o ficheiro Excel. Verifique se ele está fechado. Erro: {e}")
        return

    # 2. Ligar à Base de Dados SQLite
    conn = sqlite3.connect(CAMINHO_BANCO)
    cursor = conn.cursor()

    print("A migrar Clientes...")
    for _, linha in df_clientes.iterrows():
        nome = str(linha.get("Nome", "")).strip()
        if nome and nome.lower() != "nan":
            # INSERT OR IGNORE evita erros se o cliente já existir
            cursor.execute("INSERT OR IGNORE INTO clientes (nome) VALUES (?)", (nome,))

    print("A migrar Estoque...")
    for _, linha in df_estoque.iterrows():
        nome_produto = str(linha.get("Nome do produto", "")).strip()
        tamanho = str(linha.get("Tamanho", "")).strip()
        
        # Lida com valores vazios (NaN) que vêm do Pandas
        qtd = linha.get("Quantidade", 0)
        quantidade = int(qtd) if pd.notna(qtd) else 0
        
        val = linha.get("Valor unitario compra", 0)
        valor_compra = float(val) if pd.notna(val) else 0.0

        if nome_produto and nome_produto.lower() != "nan":
            cursor.execute("""
                INSERT OR IGNORE INTO estoque (nome_produto, tamanho, quantidade, valor_compra)
                VALUES (?, ?, ?, ?)
            """, (nome_produto, tamanho, quantidade, valor_compra))

    # Funções auxiliares para buscar os IDs para as Tabelas Relacionais
    def obter_id_cliente(nome_cliente):
        cursor.execute("SELECT id FROM clientes WHERE nome = ?", (nome_cliente,))
        resultado = cursor.fetchone()
        return resultado[0] if resultado else None

    def obter_id_estoque(nome_produto, tamanho):
        cursor.execute("SELECT id FROM estoque WHERE nome_produto = ? AND tamanho = ?", (nome_produto, tamanho))
        resultado = cursor.fetchone()
        return resultado[0] if resultado else None

    print("A migrar Vendas históricas...")
    for _, linha in df_vendas.iterrows():
        cliente_nome = str(linha.get("Cliente", "")).strip()
        nome_produto = str(linha.get("Nome do produto", "")).strip()
        tamanho = str(linha.get("Tamanho", "")).strip()
        data_venda = str(linha.get("Data", ""))
        
        qtd = linha.get("Quantidade", 0)
        quantidade = int(qtd) if pd.notna(qtd) else 0
        
        val = linha.get("Valor unitario venda", 0)
        valor_unitario = float(val) if pd.notna(val) else 0.0

        cliente_id = obter_id_cliente(cliente_nome)
        estoque_id = obter_id_estoque(nome_produto, tamanho)

        # Só insere a venda se encontrar o cliente e o produto na base de dados
        if cliente_id and estoque_id:
            cursor.execute("""
                INSERT INTO vendas (cliente_id, estoque_id, quantidade, valor_unitario, data_venda)
                VALUES (?, ?, ?, ?, ?)
            """, (cliente_id, estoque_id, quantidade, valor_unitario, data_venda))
        else:
            print(f"Aviso: Venda ignorada (Cliente '{cliente_nome}' ou Produto '{nome_produto}' não encontrados).")

    # Guarda as alterações e fecha a ligação
    conn.commit()
    conn.close()
    
    print("Migração concluída com SUCESSO! A sua base de dados está pronta.")

if __name__ == "__main__":
    executar_migracao()
