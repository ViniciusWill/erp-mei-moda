from .base_repository import BaseRepository
from app.models.Estoque_model import Estoque


class EstoqueRepository(BaseRepository):

    def buscar_por_id(self, estoque_id: int):
        row = self.executar_select_um(
            "SELECT * FROM estoque WHERE id = ?", (estoque_id,)
        )
        if row:
            return Estoque(**dict(row))
        return None

    def buscar_todos(self):
        rows = self.executar_select("SELECT * FROM estoque")
        return [Estoque(**dict(row)) for row in rows]

    def buscar_por_nome(self, nome_produto: str):
        row = self.executar_select_um(
            "SELECT * FROM estoque WHERE nome_produto = ?", (nome_produto,)
        )
        if row:
            return Estoque(**dict(row))
        return None

    def cadastra_novo_produto(self, estoque: Estoque):
        return self.executar_insert(
            """INSERT INTO estoque (nome_produto, tamanho, quantidade, valor_compra)
               VALUES (?, ?, ?, ?)""",
            (estoque.nome_produto, estoque.tamanho, estoque.quantidade, estoque.valor_compra),
        )
    def inserir_produto(self, nome: str, tamanho: str, quantidade: int, valor_unitario: float):
        return self.executar_insert(
        """INSERT INTO estoque (nome_produto, tamanho, quantidade, valor_compra)
           VALUES (?, ?, ?, ?)""",
        (nome, tamanho, quantidade, valor_unitario),
    )