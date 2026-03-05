from src.database.Participantes_repository import ParticipantesRepository
from src.models.Participantes_model import Participante


class ParticipanteService:
    def __init__(self):
        self.participante_repo = ParticipantesRepository()

    def LançamentoParticipanteCampoObrigatorio(self, nome: str):
        try:    
            novo_participante = Participante(nome=nome)
            self.participante_repo.LançamentoParticipanteCampoObrigatorio(novo_participante)
        except Exception as e: 
           raise e
            