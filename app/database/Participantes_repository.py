from sqlalchemy import select

from app.database.base_repository import BaseRepository
from app.database.orm_models import Participante as ParticipanteORM
from app.models import Participante


class ParticipantesRepository(BaseRepository):

    def lancamento_participante(self, participante: Participante):
        with self._session() as session:
            novo = ParticipanteORM(nome=participante.nome, cnpj=participante.cnpj)
            session.add(novo)
            session.flush()
            return novo.id

    def inserir_participante(self, nome: str, cnpj: str | None = None, tipo: str | None = None):
        with self._session() as session:
            novo = ParticipanteORM(nome=nome, cnpj=cnpj)
            session.add(novo)
            session.flush()
            return novo.id

    def buscar_todos(self):
        with self._session() as session:
            rows = session.execute(select(ParticipanteORM)).scalars().all()
            return [{"id": r.id, "nome": r.nome, "cnpj": r.cnpj} for r in rows]

    def buscar_por_id(self, participante_id: int):
        with self._session() as session:
            row = session.get(ParticipanteORM, participante_id)
            if row:
                return {"id": row.id, "nome": row.nome, "cnpj": row.cnpj}
            return None

    def excluir(self, participante):
        with self._session() as session:
            row = session.get(ParticipanteORM, participante["id"])
            if row:
                session.delete(row)
