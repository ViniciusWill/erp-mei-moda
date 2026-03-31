from .base_repository import BaseRepository
from app.models.Estoque_model import Estoque 

class EstoqueRepository(BaseRepository):
    def buscar_por_id(self, estoque_id: int):
        """Busca um produto específico pelo ID no banco de dados."""
        query = "SELECT * FROM estoque WHERE id = ?"
        rows = self.executar_select(query, (estoque_id,))
        
        if rows:
            row = rows[0]
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
        query = "SELECT * FROM estoque"
        rows = self.executar_select(query)
        return [Estoque(**dict(row)) for row in rows]
    def buscar_por_nome(self, nome_produto: str):
        """Busca um produto específico pelo nome."""
        query = "SELECT * FROM estoque WHERE nome_produto = ?"
        rows = self.executar_select(query, (nome_produto,))
        if rows:
            row = rows[0]
            return Estoque(
                id=row["id"],
                nome_produto=row["nome_produto"], 
                tamanho=row["tamanho"],
                quantidade=row["quantidade"],
                valor_compra=row["valor_compra"]
            )
        return None
    def cadastra_novo_produto(self, estoque: Estoque):
        """Cadastra um novo produto no estoque e retorna o ID gerado"""
        conn = self._get_connection()
        try:
            with conn: 
                cur = conn.cursor()
                query = """
                    INSERT INTO estoque (nome_produto, tamanho, quantidade, valor_compra) 
                    VALUES (?, ?, ?, ?)
                """
                params = (estoque.nome_produto, estoque.tamanho, estoque.quantidade, estoque.valor_compra)
                
                if self.db_url:
                    query = query.replace("?", "%s")
                    query += " RETURNING id" 
                    cur.execute(query, params)
                    novo_id = cur.fetchone()['id']
                else:
                    cur.execute(query, params)
                    novo_id = cur.lastrowid                   
                return novo_id
        except Exception as e:
            print(f"Erro ao cadastrar produto: {e}")
            raise e 
        finally:
            conn.close() 