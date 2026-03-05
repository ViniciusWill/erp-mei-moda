from .base_repository import BaseRepository
from src.models import Participante

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
