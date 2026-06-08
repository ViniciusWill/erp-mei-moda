"""initial schema — todas as tabelas base

Revision ID: 0001
Revises:
Create Date: 2026-06-08

Migration raiz: cria todas as tabelas base usando IF NOT EXISTS (idempotente).
Em bancos existentes, as tabelas ja existem e nada muda.
Em bancos novos, tudo e criado aqui antes das migrations incrementais.
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = '0001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _tabelas_existentes():
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    return set(inspector.get_table_names())


def upgrade() -> None:
    existentes = _tabelas_existentes()

    if 'clientes' not in existentes:
        op.create_table(
            'clientes',
            sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
            sa.Column('nome', sa.Text(), nullable=False),
            sa.Column('cpf', sa.String(11), nullable=True),
            sa.UniqueConstraint('nome'),
        )

    if 'estoque' not in existentes:
        op.create_table(
            'estoque',
            sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
            sa.Column('nome_produto', sa.Text(), nullable=False),
            sa.Column('tamanho', sa.Text(), nullable=False),
            sa.Column('quantidade', sa.Integer(), nullable=False),
            sa.Column('valor_compra', sa.Float(), nullable=False),
            sa.UniqueConstraint('nome_produto', 'tamanho'),
        )

    if 'participantes' not in existentes:
        op.create_table(
            'participantes',
            sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
            sa.Column('nome', sa.Text(), nullable=False),
            sa.Column('cnpj', sa.String(14), nullable=True),
            sa.UniqueConstraint('nome'),
        )

    if 'vendas' not in existentes:
        op.create_table(
            'vendas',
            sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
            sa.Column('cliente_id', sa.Integer(), nullable=False),
            sa.Column('estoque_id', sa.Integer(), nullable=False),
            sa.Column('quantidade', sa.Integer(), nullable=False),
            sa.Column('valor_unitario', sa.Float(), nullable=False),
            sa.Column('data_venda', sa.String(), nullable=False),
            sa.ForeignKeyConstraint(['cliente_id'], ['clientes.id']),
            sa.ForeignKeyConstraint(['estoque_id'], ['estoque.id']),
        )

    if 'compras' not in existentes:
        op.create_table(
            'compras',
            sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
            sa.Column('estoque_id', sa.Integer(), nullable=False),
            sa.Column('fornecedor_id', sa.Integer(), nullable=False),
            sa.Column('quantidade', sa.Integer(), nullable=False),
            sa.Column('valor_unitario', sa.Float(), nullable=False),
            sa.Column('data_compra', sa.String(), nullable=False),
            sa.ForeignKeyConstraint(['estoque_id'], ['estoque.id']),
            sa.ForeignKeyConstraint(['fornecedor_id'], ['participantes.id']),
        )

    if 'contas_a_pagar' not in existentes:
        op.create_table(
            'contas_a_pagar',
            sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
            sa.Column('compra_id', sa.Integer(), nullable=False),
            sa.Column('parcela', sa.Integer(), nullable=False),
            sa.Column('valor_parcela', sa.Float(), nullable=False),
            sa.Column('valor_pendente', sa.Float(), nullable=False),
            sa.Column('data_vencimento', sa.String(), nullable=False),
            sa.ForeignKeyConstraint(['compra_id'], ['compras.id']),
        )

    if 'contas_a_receber' not in existentes:
        op.create_table(
            'contas_a_receber',
            sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
            sa.Column('venda_id', sa.Integer(), nullable=False),
            sa.Column('parcela', sa.Integer(), nullable=False),
            sa.Column('valor_parcela', sa.Float(), nullable=False),
            sa.Column('valor_pendente', sa.Float(), nullable=False),
            sa.Column('data_vencimento', sa.String(), nullable=False),
            sa.ForeignKeyConstraint(['venda_id'], ['vendas.id']),
        )

    if 'usuarios' not in existentes:
        op.create_table(
            'usuarios',
            sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
            sa.Column('nome', sa.Text(), nullable=False),
            sa.Column('cpf', sa.String(11), nullable=True),
            sa.Column('cnpj', sa.String(18), nullable=True),
            sa.Column('email', sa.String(255), nullable=False),
            sa.Column('senha_hash', sa.String(255), nullable=False),
            sa.Column('role', sa.String(50), server_default='operador', nullable=False),
        )

    if 'recuperacao_senha' not in existentes:
        op.create_table(
            'recuperacao_senha',
            sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
            sa.Column('usuario_id', sa.Integer(), nullable=False),
            sa.Column('codigo_hash', sa.String(255), nullable=False),
            sa.Column('expira_em', sa.String(), nullable=False),
            sa.Column('usado_em', sa.String(), nullable=True),
            sa.Column('criado_em', sa.String(), nullable=False),
            sa.ForeignKeyConstraint(['usuario_id'], ['usuarios.id']),
        )

    if 'emails_autorizados' not in existentes:
        op.create_table(
            'emails_autorizados',
            sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
            sa.Column('email', sa.String(255), nullable=False),
            sa.Column('usado', sa.Integer(), server_default='0', nullable=False),
            sa.Column('criado_em', sa.String(), nullable=False),
            sa.UniqueConstraint('email'),
        )


def downgrade() -> None:
    # Migration inicial — sem downgrade
    pass
