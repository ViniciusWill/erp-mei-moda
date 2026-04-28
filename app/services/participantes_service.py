from app.database.Participantes_repository import ParticipantesRepository
from app.models.Participantes_model import Participante


class ParticipanteService:
    def __init__(self):
        self.participante_repo = ParticipantesRepository()

    def lancamento_participante(self, nome: str, cnpj: str = ""):
        novo_participante = Participante(nome=nome, cnpj=cnpj)
        self.participante_repo.lancamento_participante(novo_participante)

    def excluir_participante(self, participante_id: int):
        participante = self.participante_repo.buscar_por_id(participante_id)
        if not participante:
            raise ValueError("Participante não encontrado.")
        self.participante_repo.excluir(participante)
