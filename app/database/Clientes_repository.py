from sqlalchemy import select, func

from app.database.base_repository import BaseRepository
from app.database.orm_models import Cliente as ClienteORM


class ClienteRepository(BaseRepository):

    def salvar(self, cliente):
        with self._session() as session:
            novo = ClienteORM(nome=cliente.nome, cpf=cliente.cpf)
            session.add(novo)
            session.flush()
            return novo.id

    def inserir_cliente(self, nome: str, cpf: str | None = None):
        with self._session() as session:
            novo = ClienteORM(nome=nome, cpf=cpf)
            session.add(novo)
            session.flush()
            return novo.id

    def buscar_todos(self):
        with self._session() as session:
            rows = session.execute(select(ClienteORM)).scalars().all()
            return [{"id": r.id, "nome": r.nome, "cpf": r.cpf} for r in rows]

    def buscar_por_nome(self, nome: str):
        with self._session() as session:
            stmt = select(ClienteORM).where(func.lower(ClienteORM.nome) == nome.lower())
            row = session.execute(stmt).scalar_one_or_none()
            if row:
                return {"id": row.id, "nome": row.nome, "cpf": row.cpf}
            return None

    def buscar_por_id(self, cliente_id: int):
        with self._session() as session:
            row = session.get(ClienteORM, cliente_id)
            if row:
                return {"id": row.id, "nome": row.nome, "cpf": row.cpf}
            return None

    def excluir(self, cliente):
        with self._session() as session:
            row = session.get(ClienteORM, cliente["id"])
            if row:
                session.delete(row)
