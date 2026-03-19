from .base_repository import BaseRepository
from app.models import Participante

class ParticipantesRepository(BaseRepository):
    def LançamentoParticipanteCampoObrigatorio(self, participante: Participante):
        with self.__conection__() as conn:
            try:
                cur = conn.cursor()
                cur.execute("""INSERT INTO Participantes (nome) VALUES (?)""", (participante.nome,))
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise e
    def buscar_todos(self):
        with self.__conection__() as conn:
           cur = conn.cursor()
           cur.execute("SELECT * FROM Participantes")
           rows = cur.fetchall()
        return [{"id": row["id"], "nome": row["nome"]} for row in rows]
