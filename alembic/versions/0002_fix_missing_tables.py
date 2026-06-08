"""fix tabelas ausentes e PK de usuarios

Revision ID: 0002
Revises: 99f45b3e9c92
Create Date: 2026-06-08

Correcao para bancos de producao criados antes do Alembic:
- Garante que usuarios.id tem PRIMARY KEY (necessario para FK de recuperacao_senha)
- Cria recuperacao_senha se nao existir
- Cria emails_autorizados se nao existir (migration 99f45b3e9c92 era no-op)
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = '0002'
down_revision: Union[str, None] = '99f45b3e9c92'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    existentes = set(inspector.get_table_names())

    # --- Garante que usuarios.id tem PRIMARY KEY (PostgreSQL) ---
    if conn.dialect.name == 'postgresql':
        resultado = conn.execute(sa.text(
            "SELECT 1 FROM information_schema.table_constraints "
            "WHERE table_name = 'usuarios' AND constraint_type = 'PRIMARY KEY'"
        )).fetchone()
        if not resultado:
            op.execute(sa.text("ALTER TABLE usuarios ADD PRIMARY KEY (id)"))

    # --- Cria recuperacao_senha se nao existir ---
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

    # --- Cria emails_autorizados se nao existir ---
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
    pass
