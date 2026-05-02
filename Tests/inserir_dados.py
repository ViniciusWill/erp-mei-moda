import sqlite3
import sys
from datetime import datetime, timedelta
from pathlib import Path

import psycopg2

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.database.db_config import normalizar_database_url, obter_database_url


def conectar_banco():
    database_url = obter_database_url()

    if database_url:
        url = normalizar_database_url(database_url)
        return psycopg2.connect(url), True

    caminho_banco = Path(__file__).resolve().parent.parent / "dados" / "sistema_loja.db"
    conn = sqlite3.connect(caminho_banco)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn, False


def adaptar_query(query: str, is_postgres: bool) -> str:
    return query.replace("?", "%s") if is_postgres else query


def buscar_ou_criar(cursor, is_postgres: bool, tabela: str, coluna: str, valor):
    cursor.execute(
        adaptar_query(f"SELECT id FROM {tabela} WHERE {coluna} = ?", is_postgres),
        (valor,),
    )
    existente = cursor.fetchone()
    if existente:
        return existente[0]

    cursor.execute(
        adaptar_query(f"INSERT INTO {tabela} ({coluna}) VALUES (?)", is_postgres),
        (valor,),
    )

    cursor.execute(
        adaptar_query(f"SELECT id FROM {tabela} WHERE {coluna} = ?", is_postgres),
        (valor,),
    )
    criado = cursor.fetchone()
    return criado[0]


def popular_banco():
    try:
        conn, is_postgres = conectar_banco()
        cur = conn.cursor()
        print("Conectando ao banco para insercao...")

        fornecedor_id = buscar_ou_criar(cur, is_postgres, "Participantes", "nome", "Fornecedor Alpha")
        cliente_id = buscar_ou_criar(cur, is_postgres, "clientes", "nome", "Joao Silva")

        cur.execute(
            adaptar_query(
                """
                SELECT id FROM estoque
                WHERE nome_produto = ? AND tamanho = ?
                """,
                is_postgres,
            ),
            ("Camiseta Polo", "G"),
        )
        estoque_existente = cur.fetchone()

        if estoque_existente:
            produto_id = estoque_existente[0]
        else:
            cur.execute(
                adaptar_query(
                    """
                    INSERT INTO estoque (nome_produto, tamanho, quantidade, valor_compra)
                    VALUES (?, ?, ?, ?)
                    """,
                    is_postgres,
                ),
                ("Camiseta Polo", "G", 50, 25.50),
            )
            cur.execute(
                adaptar_query(
                    """
                    SELECT id FROM estoque
                    WHERE nome_produto = ? AND tamanho = ?
                    """,
                    is_postgres,
                ),
                ("Camiseta Polo", "G"),
            )
            produto_id = cur.fetchone()[0]

        agora = datetime.now()
        agora_str = agora.isoformat(sep=" ", timespec="seconds")
        vencimento_str = (agora + timedelta(days=30)).isoformat(sep=" ", timespec="seconds")

        cur.execute(
            adaptar_query(
                """
                SELECT 1 FROM compras
                WHERE estoque_id = ? AND fornecedor_id = ? AND quantidade = ?
                """,
                is_postgres,
            ),
            (produto_id, fornecedor_id, 10),
        )
        if not cur.fetchone():
            cur.execute(
                adaptar_query(
                    """
                    INSERT INTO compras (estoque_id, fornecedor_id, quantidade, valor_unitario, data_compra)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    is_postgres,
                ),
                (produto_id, fornecedor_id, 10, 20.00, agora_str),
            )
            cur.execute(
                adaptar_query(
                    """
                    SELECT id FROM compras
                    WHERE estoque_id = ? AND fornecedor_id = ? AND quantidade = ?
                    ORDER BY id DESC
                    LIMIT 1
                    """,
                    is_postgres,
                ),
                (produto_id, fornecedor_id, 10),
            )
            compra = cur.fetchone()
            compra_id = compra[0]
            cur.execute(
                adaptar_query(
                    """
                    INSERT INTO contas_a_pagar (compra_id, parcela, valor_parcela, valor_pendente, data_vencimento)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    is_postgres,
                ),
                (compra_id, 1, 200.00, 200.00, vencimento_str),
            )

        cur.execute(
            adaptar_query(
                """
                SELECT 1 FROM vendas
                WHERE cliente_id = ? AND estoque_id = ? AND quantidade = ?
                """,
                is_postgres,
            ),
            (cliente_id, produto_id, 2),
        )
        if not cur.fetchone():
            cur.execute(
                adaptar_query(
                    """
                    INSERT INTO vendas (cliente_id, estoque_id, quantidade, valor_unitario, data_venda)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    is_postgres,
                ),
                (cliente_id, produto_id, 2, 80.00, agora_str),
            )
            cur.execute(
                adaptar_query(
                    """
                    SELECT id FROM vendas
                    WHERE cliente_id = ? AND estoque_id = ? AND quantidade = ?
                    ORDER BY id DESC
                    LIMIT 1
                    """,
                    is_postgres,
                ),
                (cliente_id, produto_id, 2),
            )
            venda = cur.fetchone()
            venda_id = venda[0]
            cur.execute(
                adaptar_query(
                    """
                    INSERT INTO contas_a_receber (venda_id, parcela, valor_parcela, valor_pendente, data_vencimento)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    is_postgres,
                ),
                (venda_id, 1, 160.00, 160.00, vencimento_str),
            )

        conn.commit()
        print("Dados iniciais verificados com sucesso.")

    except Exception as e:
        print(f"Erro ao inserir dados: {e}")
        if "conn" in locals():
            conn.rollback()
        raise
    finally:
        if "cur" in locals():
            cur.close()
        if "conn" in locals():
            conn.close()


if __name__ == "__main__":
    popular_banco()
