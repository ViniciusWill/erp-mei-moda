import sqlite3
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import create_app
from app.database import db_config
from app.database.Compras_repository import CompraRepository
from app.database.orm_models import Base, Cliente, EmailAutorizado, Estoque, Participante
from app.routes import auth_routes


@pytest.fixture()
def client(monkeypatch):
    temp_dir = Path("Tests") / ".tmp"
    temp_dir.mkdir(exist_ok=True)
    db_path = temp_dir / f"test_loja_{uuid.uuid4().hex}.db"

    # Cria engine e tabelas usando os modelos ORM (inclui role, emails_autorizados etc.)
    test_engine = create_engine(
        f"sqlite:///{db_path}",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(test_engine)
    TestSessionLocal = sessionmaker(bind=test_engine, autocommit=False, autoflush=False)

    # Injeta a factory de teste em todos os repositories
    monkeypatch.setattr(db_config, "_override_session_factory", TestSessionLocal)

    # Dados base + emails pré-autorizados para os testes de cadastro
    agora = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with Session(test_engine) as s:
        s.add(Cliente(nome="Cliente Base", cpf="12345678901"))
        s.add(Estoque(nome_produto="Camiseta Polo", tamanho="G", quantidade=10, valor_compra=25.50))
        s.add(Participante(nome="Fornecedor Base", cnpj="12345678000199"))
        s.add(EmailAutorizado(email="primeiro@teste.com", usado=0, criado_em=agora))
        s.add(EmailAutorizado(email="outro@teste.com",   usado=0, criado_em=agora))
        s.commit()

    app = create_app()
    app.config.update(TESTING=True)

    try:
        with app.test_client() as test_client:
            # Simula usuário logado para todas as rotas protegidas por @login_required
            with test_client.session_transaction() as sess:
                sess["usuario_id"] = 1
                sess["usuario_role"] = "operador"
            yield test_client, db_path
    finally:
        # Fecha conexões do SQLAlchemy antes de deletar o arquivo (necessário no Windows)
        test_engine.dispose()
        try:
            if db_path.exists():
                db_path.unlink()
        except PermissionError:
            pass  # arquivo ainda em uso, cleanup feito pelo OS


# ---------------------------------------------------------------------------
# Helpers para leitura direta no SQLite
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Testes
# ---------------------------------------------------------------------------

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


def test_primeiro_acesso_cliente_cadastra_usuario_sem_login(client):
    test_client, db_path = client

    response = test_client.post(
        "/auth/cadastrar-cliente",
        data={
            "nome": "Usuario Primeiro Acesso",
            "email": "primeiro@teste.com",
            "cpf": "11122233344",
            "cnpj": "",
            "senha": "senha123",
            "confirmar_senha": "senha123",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302
    usuario = fetch_one(
        db_path,
        "SELECT nome, email, cpf, senha_hash FROM usuarios WHERE email = ?",
        ("primeiro@teste.com",),
    )
    cliente = fetch_one(db_path, "SELECT nome FROM clientes WHERE nome = ?", ("Usuario Primeiro Acesso",))
    assert usuario[:3] == ("Usuario Primeiro Acesso", "primeiro@teste.com", "11122233344")
    assert check_password_hash(usuario[3], "senha123")
    assert cliente is None


def test_primeiro_acesso_usuario_duplicado_mostra_mensagem_amigavel(client):
    test_client, db_path = client

    # Insere usuário direto no banco (sem passar pela rota de cadastro)
    conn = sqlite3.connect(db_path)
    try:
        conn.execute(
            "INSERT INTO usuarios (nome, cpf, cnpj, email, senha_hash) VALUES (?, ?, ?, ?, ?)",
            ("Usuario Base", "11122233344", "", "base@teste.com", generate_password_hash("senha123")),
        )
        conn.commit()
    finally:
        conn.close()

    # Tenta cadastrar outro usuário com o mesmo nome (email diferente, já pré-autorizado)
    response = test_client.post(
        "/auth/cadastrar-cliente",
        data={
            "nome": "Usuario Base",
            "email": "outro@teste.com",
            "cpf": "99988877766",
            "senha": "senha123",
            "confirmar_senha": "senha123",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert "Ja existe um usuario cadastrado com esse nome." in response.get_data(as_text=True)
    assert "UNIQUE constraint failed" not in response.get_data(as_text=True)


def test_visitante_acessa_erp_com_temporizador_e_sem_rodape_na_home(client):
    test_client, _ = client

    response = test_client.get("/auth/visitante", follow_redirects=False)

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")

    home = test_client.get("/")
    estoque = test_client.get("/estoque")

    assert home.status_code == 200
    assert "temporizador-visitante" in home.get_data(as_text=True)
    assert "rodape-icones" not in home.get_data(as_text=True)
    assert estoque.status_code == 200
    assert "temporizador-visitante" in estoque.get_data(as_text=True)
    assert "rodape-icones" in estoque.get_data(as_text=True)


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
        "SELECT nome FROM participantes WHERE nome = ?",
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
        "SELECT nome, cnpj FROM participantes WHERE nome = ?",
        ("Fornecedor Compra",),
    )
    assert fornecedor == ("Fornecedor Compra", "11222333000144")


def test_recuperacao_de_senha_envia_codigo_e_atualiza_senha(client, monkeypatch):
    test_client, db_path = client
    codigo_enviado = {}

    conn = sqlite3.connect(db_path)
    try:
        conn.execute(
            "INSERT INTO usuarios (nome, cpf, cnpj, email, senha_hash) VALUES (?, ?, ?, ?, ?)",
            ("Usuario Teste", "12345678901", "", "usuario@teste.com", generate_password_hash("senha-antiga")),
        )
        conn.commit()
    finally:
        conn.close()

    def fake_enviar_email(destinatario, codigo):
        codigo_enviado["destinatario"] = destinatario
        codigo_enviado["codigo"] = codigo

    monkeypatch.setattr(auth_routes, "enviar_email_recuperacao", fake_enviar_email)

    response = test_client.post(
        "/auth/esquecisenha",
        data={"email": "usuario@teste.com"},
        follow_redirects=False,
    )
    assert response.status_code == 302
    assert codigo_enviado["destinatario"] == "usuario@teste.com"

    response = test_client.post(
        "/auth/verificar-codigo",
        data={"email": "usuario@teste.com", "codigo": codigo_enviado["codigo"]},
        follow_redirects=False,
    )
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/auth/nova-senha")

    response = test_client.post(
        "/auth/nova-senha",
        data={"senha": "senha-nova", "confirmar_senha": "senha-nova"},
        follow_redirects=False,
    )
    assert response.status_code == 302

    senha_hash = fetch_one(db_path, "SELECT senha_hash FROM usuarios WHERE email = ?", ("usuario@teste.com",))[0]
    codigo_usado = fetch_one(db_path, "SELECT usado_em FROM recuperacao_senha WHERE usuario_id = 1")[0]
    assert check_password_hash(senha_hash, "senha-nova")
    assert codigo_usado is not None


def test_rotas_financeiras_renderizam_templates(client):
    test_client, _ = client

    assert test_client.get("/financeiro/contas_pagar").status_code == 200
    assert test_client.get("/financeiro/contas_receber").status_code == 200


def test_rotas_get_principais_renderizam_templates(client):
    test_client, _ = client

    rotas = [
        "/",
        "/clientes",
        "/clientes/novo",
        "/compras",
        "/compras/novo-produto",
        "/compras/novo-fornecedor",
        "/estoque",
        "/participantes",
        "/participantes/novo",
        "/relatorios",
        "/vendas",
        "/vendas/novo-cliente",
        "/financeiro/contas_pagar",
        "/financeiro/contas_receber",
        "/auth/esquecisenha",
    ]

    for rota in rotas:
        resp = test_client.get(rota)
        assert resp.status_code == 200, f"Falhou em: {rota}"


def test_relatorio_de_compras_retorna_todos_os_registros(client):
    _, db_path = client

    conn = sqlite3.connect(db_path)
    try:
        conn.execute(
            "INSERT INTO compras (estoque_id, fornecedor_id, quantidade, valor_unitario, data_compra) VALUES (?, ?, ?, ?, ?)",
            (1, 1, 2, 25.5, "2026-04-12 09:00:00"),
        )
        conn.execute(
            "INSERT INTO compras (estoque_id, fornecedor_id, quantidade, valor_unitario, data_compra) VALUES (?, ?, ?, ?, ?)",
            (1, 1, 4, 25.5, "2026-04-12 10:00:00"),
        )
        conn.commit()
    finally:
        conn.close()

    compras = CompraRepository().selecionar_todas_compras()

    assert len(compras) == 2
    assert [c["quantidade"] for c in compras] == [2, 4]


def test_excluir_compra_remove_parcelas_vinculadas(client):
    test_client, db_path = client

    response = test_client.post(
        "/compras",
        data={"fornecedor_id": "1", "estoque_id": "1", "quantidade": "3", "parcelas": "2"},
        follow_redirects=False,
    )
    assert response.status_code == 302

    compra_id = fetch_one(db_path, "SELECT id FROM compras ORDER BY id DESC LIMIT 1")[0]
    assert len(fetch_all(db_path, "SELECT id FROM contas_a_pagar WHERE compra_id = ?", (compra_id,))) == 2

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
    assert len(fetch_all(db_path, "SELECT id FROM contas_a_receber WHERE venda_id = ?", (venda_id,))) == 2

    response = test_client.post(f"/relatorios/venda/{venda_id}", follow_redirects=False)

    assert response.status_code == 302
    assert fetch_one(db_path, "SELECT id FROM vendas WHERE id = ?", (venda_id,)) is None
    assert fetch_all(db_path, "SELECT id FROM contas_a_receber WHERE venda_id = ?", (venda_id,)) == []
