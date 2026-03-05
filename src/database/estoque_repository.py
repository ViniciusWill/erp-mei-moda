from .base_repository import BaseRepository
from src.models.Estoque_model import Estoque 


class EstoqueRepository(BaseRepository):
    def buscar_por_id(self, estoque_id: int):
        """Busca um produto específico pelo ID no banco de dados."""
        with self.__conection__() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM estoque WHERE id = ?", (estoque_id,))
            row = cur.fetchone()
            
            if row:
                return Estoque(
                    id=row["id"],
                    nome_produto=row["nome_produto"],
                    tamanho=row["tamanho"],
                    quantidade=row["quantidade"],
                    valor_compra=row["valor_compra"]
                )
            return None

    def buscar_todos(self):
        """Retorna a lista de todos os produtos para conferência."""
        with self.__conection__() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM estoque")
            rows = cur.fetchall()
            return [Estoque(**dict(row)) for row in rows]
        
    def buscar_por_nome(self, nome_produto: str):
        with self.__conection__() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM estoque WHERE nome_produto = ?", (nome_produto,))
        row = cur.fetchone()
        if row:
            return Estoque(
                id=row["id"],
                nome_produto=row["nome_produto"], 
                tamanho=row["tamanho"],
                quantidade=row["quantidade"],
                valor_compra=row["valor_compra"]
            )
        return None
    def cadastra_novo_produto(self, estoque: Estoque):
        
        """Cadastra um novo produto no estoque"""
        with self.__conection__() as conn:
            try:
                cur = conn.cursor()
                cur.execute("""INSERT INTO estoque (nome_produto, tamanho, quantidade, valor_compra) VALUES (?, ?, ?, ?)""", 
                                                    (estoque.nome_produto, 
                                                     estoque.tamanho,
                                                     estoque.quantidade, 
                                                     estoque.valor_compra))
                conn.commit()
            except Exception as e:
                conn.rollback()
                print(f"erro: {e} ")
        return cur.lastrowid