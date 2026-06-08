from sqlalchemy import select

from app.database.base_repository import BaseRepository
from app.database.orm_models import Estoque as EstoqueORM
from app.models.Estoque_model import Estoque


class EstoqueRepository(BaseRepository):

    def buscar_por_id(self, estoque_id: int):
        with self._session() as session:
            row = session.get(EstoqueORM, estoque_id)
            if row:
                return Estoque(
                    id=row.id,
                    nome_produto=row.nome_produto,
                    tamanho=row.tamanho,
                    quantidade=row.quantidade,
                    valor_compra=row.valor_compra,
                )
            return None

    def buscar_todos(self):
        with self._session() as session:
            rows = session.execute(select(EstoqueORM)).scalars().all()
            return [
                Estoque(
                    id=r.id,
                    nome_produto=r.nome_produto,
                    tamanho=r.tamanho,
                    quantidade=r.quantidade,
                    valor_compra=r.valor_compra,
                )
                for r in rows
            ]

    def buscar_por_nome(self, nome_produto: str):
        with self._session() as session:
            stmt = select(EstoqueORM).where(EstoqueORM.nome_produto == nome_produto)
            row = session.execute(stmt).scalar_one_or_none()
            if row:
                return Estoque(
                    id=row.id,
                    nome_produto=row.nome_produto,
                    tamanho=row.tamanho,
                    quantidade=row.quantidade,
                    valor_compra=row.valor_compra,
                )
            return None

    def cadastra_novo_produto(self, estoque: Estoque):
        with self._session() as session:
            novo = EstoqueORM(
                nome_produto=estoque.nome_produto,
                tamanho=estoque.tamanho,
                quantidade=estoque.quantidade,
                valor_compra=estoque.valor_compra,
            )
            session.add(novo)
            session.flush()
            return novo.id

    def inserir_produto(self, nome: str, tamanho: str, quantidade: int, valor_unitario: float):
        with self._session() as session:
            novo = EstoqueORM(
                nome_produto=nome,
                tamanho=tamanho,
                quantidade=quantidade,
                valor_compra=valor_unitario,
            )
            session.add(novo)
            session.flush()
            return novo.id
