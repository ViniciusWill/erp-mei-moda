from .base_repository import BaseRepository
from app.models import Participante
 
 
class ParticipantesRepository(BaseRepository):
 
    def lancamento_participante(self, participante: Participante):
        self.executar_insert(
            "INSERT INTO Participantes (nome) VALUES (?)", (participante.nome,)
        )
 
    def buscar_todos(self):
        rows = self.executar_select("SELECT * FROM Participantes")
        return [{"id": row["id"], "nome": row["nome"]} for row in rows]