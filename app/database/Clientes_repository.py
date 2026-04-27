from .base_repository import BaseRepository
from app.models.Clientes_model import Cliente


class ClienteRepository(BaseRepository):

    def salvar(self, cliente: Cliente):
        return self.executar_insert(
            "INSERT INTO clientes (nome, cpf) VALUES (?, ?)", (cliente.nome, cliente.cpf)
        )

    def inserir_cliente(self, nome: str, cpf: str | None = None):
        return self.executar_insert(
            "INSERT INTO clientes (nome, cpf) VALUES (?, ?)",
            (nome, cpf),
        )

    def buscar_todos(self):
        rows = self.executar_select("SELECT * FROM clientes")
        return [{"id": row["id"], "nome": row["nome"], "cpf": row["cpf"]} for row in rows]
    
    def buscar_por_id(self, cliente_id: int):
        row = self.executar_select("SELECT * FROM clientes WHERE id = ?", (cliente_id,))
        if row:
            return {"id": row[0]["id"], "nome": row[0]["nome"], "cpf": row[0]["cpf"]}
        return None
    def excluir(self, cliente):
        self.executar_delete("DELETE FROM clientes WHERE id = ?", (cliente["id"],))
