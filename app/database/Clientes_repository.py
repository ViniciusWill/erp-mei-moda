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
    
    def buscar_por_id(self, cliente_id: int):
        row = self.executar_select("SELECT * FROM clientes WHERE id = ?", (cliente_id,))
        if row:
            return {"id": row[0]["id"], "nome": row[0]["nome"]}
        return None
    def excluir(self, cliente):
        self.executar_delete("DELETE FROM clientes WHERE id = ?", (cliente["id"],))