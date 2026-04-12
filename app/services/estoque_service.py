from app.database.estoque_repository import EstoqueRepository
from app.models.Estoque_model import Estoque

class EstoqueService: 
    def __init__(self):
        self.estoque_repo = EstoqueRepository()

    def registrar_produto_estoque(self, nome_produto: str, quantidade: str, valor_compra: float, tamanho: str):
            novo_produto = Estoque(
                    nome_produto=nome_produto,
                    tamanho=tamanho,
                    quantidade=quantidade,
                    valor_compra=valor_compra
            )
            Novoid = self.estoque_repo.cadastra_novo_produto(novo_produto)
            return Novoid
        
    
            

            
