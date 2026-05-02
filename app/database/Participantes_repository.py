from .base_repository import BaseRepository
from app.models import Participante
 
 
class ParticipantesRepository(BaseRepository):
 
    def lancamento_participante(self, participante: Participante):
        self.executar_insert(
            "INSERT INTO Participantes (nome, cnpj) VALUES (?, ?)",
            (participante.nome, participante.cnpj),
        )

    def inserir_participante(self, nome: str, cnpj: str | None = None, tipo: str | None = None):
        return self.executar_insert(
            "INSERT INTO Participantes (nome, cnpj) VALUES (?, ?)",
            (nome, cnpj),
        )

    def buscar_todos(self):
        rows = self.executar_select("SELECT * FROM Participantes")
        return [{"id": row["id"], "nome": row["nome"], "cnpj": row["cnpj"]} for row in rows]

    def buscar_por_id(self, participante_id: int):
        row = self.executar_select("SELECT * FROM participantes WHERE id = ?", (participante_id,))
        if row:
            return {"id": row[0]["id"], "nome": row[0]["nome"], "cnpj": row[0]["cnpj"]}
        return None

    def excluir(self, participante):
        self.executar_delete("DELETE FROM participantes WHERE id = ?", (participante["id"],))
