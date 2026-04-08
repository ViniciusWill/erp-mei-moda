from .base_repository import BaseRepository
from app.models.Clientes_model import Cliente


class ClienteRepository(BaseRepository):

    def salvar(self, cliente: Cliente):
        self.executar_insert(
            "INSERT INTO clientes (nome) VALUES (?)", (cliente.nome,)
        )

    def buscar_todos(self):
        rows = self.executar_select("SELECT * FROM clientes")
        return [{"id": row["id"], "nome": row["nome"]} for row in rows]