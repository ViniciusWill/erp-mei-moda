import sqlite3
import sys
import uuid
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import create_app
from app.database.Compras_repository import CompraRepository
from app.database.Vendas_repository import VendaRepository
from app.database.base_repository import BaseRepository


SCHEMA = [
    """
    CREATE TABLE clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE,
        cpf VARCHAR(11)
    )
    """,
    """
    CREATE TABLE estoque (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_produto TEXT NOT NULL,
        tamanho TEXT NOT NULL,
        quantidade INTEGER NOT NULL,
        valor_compra REAL NOT NULL,
        UNIQUE(nome_produto, tamanho)
    )
    """,
    """
    CREATE TABLE Participantes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE,
        Cnpj VARCHAR(14)
    )
    """,
    """
    CREATE TABLE compras (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        estoque_id INTEGER NOT NULL,
        fornecedor_id INTEGER NOT NULL,
        quantidade INTEGER NOT NULL,
        valor_unitario REAL NOT NULL,
        data_compra TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE vendas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER NOT NULL,
        estoque_id INTEGER NOT NULL,
        quantidade INTEGER NOT NULL,
        valor_unitario REAL NOT NULL,
        data_venda TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE contas_a_pagar (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        compra_id INTEGER NOT NULL,
        parcela INTEGER NOT NULL,
        valor_parcela REAL NOT NULL,
        valor_pendente REAL NOT NULL,
        data_vencimento TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE contas_a_receber (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        venda_id INTEGER NOT NULL,
        parcela INTEGER NOT NULL,
        valor_parcela REAL NOT NULL,
        valor_pendente REAL NOT NULL,
        data_vencimento TEXT NOT NULL
    )
    """,
]


@pytest.fixture()
def client(monkeypatch):
    temp_dir = Path("Tests") / ".tmp"
    temp_dir.mkdir(exist_ok=True)
    db_path = temp_dir / f"test_loja_{uuid.uuid4().hex}.db"

    def fake_init(self):
        self.db_url = None
        self.is_postgres = False
        self.caminho_banco = Path(db_path)

    monkeypatch.setattr(BaseRepository, "__init__", fake_init)

    conn = sqlite3.connect(db_path)
    try:
        for statement in SCHEMA:
            conn.execute(statement)

        conn.execute("INSERT INTO clientes (nome, cpf) VALUES (?, ?)", ("Cliente Base", "12345678901"))
        conn.execute(
            "INSERT INTO estoque (nome_produto, tamanho, quantidade, valor_compra) VALUES (?, ?, ?, ?)",
            ("Camiseta Polo", "G", 10, 25.50),
        )
        conn.execute("INSERT INTO Participantes (nome, Cnpj) VALUES (?, ?)", ("Fornecedor Base", "12345678000199"))
        conn.commit()
    finally:
        conn.close()

    app = create_app()
    app.config.update(TESTING=True)

    try:
        with app.test_client() as test_client:
            yield test_client, db_path
    finally:
        if db_path.exists():
            db_path.unlink()


def fetch_one(db_path, query, params=()):
    conn = sqlite3.connect(db_path)
    try:
        return conn.execute(query, params).fetchone()
    finally:
        conn.close()


def fetch_all(db_path, query, params=()):
    conn = sqlite3.connect(db_path)
    try:
        return conn.execute(query, params).fetchall()
    finally:
        conn.close()


def test_post_vendas_persiste_registro_e_atualiza_estoque(client):
    test_client, db_path = client

    response = test_client.post(
        "/vendas",
        data={"cliente_id": "1", "estoque_id": "1", "Quantidade-ven": "2", "parcelas": "1"},
        follow_redirects=False,
    )

    assert response.status_code == 302
    venda = fetch_one(db_path, "SELECT quantidade, valor_unitario FROM vendas")
    estoque = fetch_one(db_path, "SELECT quantidade FROM estoque WHERE id = 1")
    assert venda == (2, 25.5)
    assert estoque == (8,)


def test_post_compras_persiste_registro_e_atualiza_estoque(client):
    test_client, db_path = client

    response = test_client.post(
        "/compras",
        data={"fornecedor_id": "1", "estoque_id": "1", "quantidade": "3", "parcelas": "1"},
        follow_redirects=False,
    )

    assert response.status_code == 302
    compra = fetch_one(db_path, "SELECT quantidade, valor_unitario FROM compras")
    estoque = fetch_one(db_path, "SELECT quantidade FROM estoque WHERE id = 1")
    assert compra == (3, 25.5)
    assert estoque == (13,)


def test_post_clientes_persiste_registro(client):
    test_client, db_path = client

    response = test_client.post(
        "/clientes/novo",
        data={"nome": "Cliente Novo"},
        follow_redirects=False,
    )

    assert response.status_code == 302
    cliente = fetch_one(db_path, "SELECT nome FROM clientes WHERE nome = ?", ("Cliente Novo",))
    assert cliente == ("Cliente Novo",)


def test_post_participantes_persiste_registro(client):
    test_client, db_path = client

    response = test_client.post(
        "/participantes/novo",
        data={"nome": "Fornecedor Novo"},
        follow_redirects=False,
    )

    assert response.status_code == 302
    participante = fetch_one(
        db_path,
        "SELECT nome FROM Participantes WHERE nome = ?",
        ("Fornecedor Novo",),
    )
    assert participante == ("Fornecedor Novo",)


def test_post_novo_cliente_venda_persiste_cpf(client):
    test_client, db_path = client

    response = test_client.post(
        "/vendas/novo-cliente",
        data={"nome": "Cliente Venda", "cpf": "98765432100"},
        follow_redirects=False,
    )

    assert response.status_code == 302
    cliente = fetch_one(
        db_path,
        "SELECT nome, cpf FROM clientes WHERE nome = ?",
        ("Cliente Venda",),
    )
    assert cliente == ("Cliente Venda", "98765432100")


def test_post_novo_fornecedor_compra_persiste_cnpj(client):
    test_client, db_path = client

    response = test_client.post(
        "/compras/novo-fornecedor?produto_id=1",
        data={"nome": "Fornecedor Compra", "cnpj": "11222333000144"},
        follow_redirects=False,
    )

    assert response.status_code == 302
    fornecedor = fetch_one(
        db_path,
        "SELECT nome, Cnpj FROM Participantes WHERE nome = ?",
        ("Fornecedor Compra",),
    )
    assert fornecedor == ("Fornecedor Compra", "11222333000144")


def test_rotas_financeiras_renderizam_templates(client):
    test_client, _ = client

    contas_pagar = test_client.get("/financeiro/contas_pagar")
    contas_receber = test_client.get("/financeiro/contas_receber")

    assert contas_pagar.status_code == 200
    assert contas_receber.status_code == 200


def test_relatorio_de_compras_retorna_todos_os_registros(client):
    _, db_path = client

    conn = sqlite3.connect(db_path)
    try:
        conn.execute(
            """
            INSERT INTO compras (estoque_id, fornecedor_id, quantidade, valor_unitario, data_compra)
            VALUES (?, ?, ?, ?, ?)
            """,
            (1, 1, 2, 25.5, "2026-04-12 09:00:00"),
        )
        conn.execute(
            """
            INSERT INTO compras (estoque_id, fornecedor_id, quantidade, valor_unitario, data_compra)
            VALUES (?, ?, ?, ?, ?)
            """,
            (1, 1, 4, 25.5, "2026-04-12 10:00:00"),
        )
        conn.commit()
    finally:
        conn.close()

    compras = CompraRepository().selecionar_todas_compras()

    assert len(compras) == 2
    assert [compra["quantidade"] for compra in compras] == [2, 4]


def test_excluir_compra_remove_parcelas_vinculadas(client):
    test_client, db_path = client

    response = test_client.post(
        "/compras",
        data={"fornecedor_id": "1", "estoque_id": "1", "quantidade": "3", "parcelas": "2"},
        follow_redirects=False,
    )
    assert response.status_code == 302

    compra_id = fetch_one(db_path, "SELECT id FROM compras ORDER BY id DESC LIMIT 1")[0]
    parcelas_antes = fetch_all(
        db_path,
        "SELECT id FROM contas_a_pagar WHERE compra_id = ?",
        (compra_id,),
    )
    assert len(parcelas_antes) == 2

    response = test_client.post(f"/relatorios/compra/{compra_id}", follow_redirects=False)

    assert response.status_code == 302
    assert fetch_one(db_path, "SELECT id FROM compras WHERE id = ?", (compra_id,)) is None
    assert fetch_all(db_path, "SELECT id FROM contas_a_pagar WHERE compra_id = ?", (compra_id,)) == []


def test_excluir_venda_remove_parcelas_vinculadas(client):
    test_client, db_path = client

    response = test_client.post(
        "/vendas",
        data={"cliente_id": "1", "estoque_id": "1", "Quantidade-ven": "2", "parcelas": "2"},
        follow_redirects=False,
    )
    assert response.status_code == 302

    venda_id = fetch_one(db_path, "SELECT id FROM vendas ORDER BY id DESC LIMIT 1")[0]
    parcelas_antes = fetch_all(
        db_path,
        "SELECT id FROM contas_a_receber WHERE venda_id = ?",
        (venda_id,),
    )
    assert len(parcelas_antes) == 2

    response = test_client.post(f"/relatorios/venda/{venda_id}", follow_redirects=False)

    assert response.status_code == 302
    assert fetch_one(db_path, "SELECT id FROM vendas WHERE id = ?", (venda_id,)) is None
    assert fetch_all(db_path, "SELECT id FROM contas_a_receber WHERE venda_id = ?", (venda_id,)) == []
