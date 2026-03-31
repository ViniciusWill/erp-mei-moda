from .base_repository import BaseRepository
from app.models import Participante

class ParticipantesRepository(BaseRepository):
    
    def LançamentoParticipanteCampoObrigatorio(self, participante: Participante):
        """Cadastra um novo participante usando apenas o campo obrigatório (nome)."""
        query = "INSERT INTO Participantes (nome) VALUES (?)"
        self.executar_comando(query, (participante.nome,))

    def buscar_todos(self):
        """Retorna a lista de todos os participantes cadastrados."""
        query = "SELECT * FROM Participantes"
        rows = self.executar_select(query)
        return [{"id": row["id"], "nome": row["nome"]} for row in rows]