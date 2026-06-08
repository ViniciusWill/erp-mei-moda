"""add role to usuarios

Revision ID: 4a33c0effb02
Revises: 
Create Date: 2026-06-08 09:32:44.950221

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '4a33c0effb02'
down_revision: Union[str, None] = '0001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()

    if conn.dialect.name == 'postgresql':
        # ADD COLUMN IF NOT EXISTS evita erro se a coluna ja existir
        # (bancos criados pela migration 0001 ja incluem role)
        conn.execute(sa.text(
            "ALTER TABLE usuarios "
            "ADD COLUMN IF NOT EXISTS role VARCHAR(50) NOT NULL DEFAULT 'operador'"
        ))
    else:
        # SQLite nao suporta IF NOT EXISTS no ADD COLUMN — verifica manualmente
        colunas = [r[1] for r in conn.execute(sa.text("PRAGMA table_info(usuarios)")).fetchall()]
        if 'role' not in colunas:
            op.add_column('usuarios', sa.Column('role', sa.String(50), server_default='operador', nullable=False))

    op.execute(sa.text("UPDATE usuarios SET role = 'admin' WHERE nome = 'admin'"))


def downgrade() -> None:
    conn = op.get_bind()
    if conn.dialect.name != 'sqlite':
        op.drop_column('usuarios', 'role')
