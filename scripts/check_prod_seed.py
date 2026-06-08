import os
import sys
from pathlib import Path

import psycopg2
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

from app.database.db_config import normalizar_database_url


def main():
    load_dotenv(ROOT_DIR / ".env")
    database_url = os.environ.get("PROD_DATABASE_URL")

    if not database_url:
        raise RuntimeError("Defina PROD_DATABASE_URL no .env local.")

    conn = psycopg2.connect(normalizar_database_url(database_url))

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, nome, cpf
                FROM clientes
                WHERE id = 8 OR nome ILIKE %s
                ORDER BY id
                """,
                ("Joao Silva",),
            )
            clientes = cursor.fetchall()

            cursor.execute(
                """
                SELECT id, cliente_id, estoque_id, quantidade, valor_unitario, data_venda
                FROM vendas
                WHERE cliente_id = 8
                ORDER BY id
                """
            )
            vendas = cursor.fetchall()

            cursor.execute(
                """
                SELECT cr.id, cr.venda_id, cr.parcela, cr.valor_pendente, cr.data_vencimento
                FROM contas_a_receber cr
                JOIN vendas v ON v.id = cr.venda_id
                WHERE v.cliente_id = 8
                ORDER BY cr.id
                """
            )
            contas = cursor.fetchall()
    finally:
        conn.close()

    print("Clientes encontrados:")
    for cliente in clientes:
        print(f"- id={cliente[0]} nome={cliente[1]} cpf={cliente[2]}")

    print("Vendas do cliente 8:")
    for venda in vendas:
        print(
            f"- id={venda[0]} cliente_id={venda[1]} estoque_id={venda[2]} "
            f"qtd={venda[3]} valor={venda[4]} data={venda[5]}"
        )

    print("Contas a receber vinculadas ao cliente 8:")
    for conta in contas:
        print(
            f"- id={conta[0]} venda_id={conta[1]} parcela={conta[2]} "
            f"pendente={conta[3]} vencimento={conta[4]}"
        )

    if not clientes and not vendas and not contas:
        print("Nenhum dado do cliente seed foi encontrado.")


if __name__ == "__main__":
    main()
