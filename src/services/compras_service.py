from datetime import datetime
from src.models.Compras_model import Compra
from src.database.Compras_repository import CompraRepository
from src.database.estoque_repository import EstoqueRepository

class CompraService:
    def __init__(self):
        self.compra_repo = CompraRepository()
        self.estoque_repo = EstoqueRepository()

            
    def lançamento_compra(self, fornecedor_id: int, estoque_id: int, quantidade: int):
        produto_existente = self.estoque_repo.buscar_por_id(estoque_id)
        estoque_id = produto_existente.id
        qnt_atual = produto_existente.quantidade
        nova_quantidade = qnt_atual + quantidade
        valor_compra = produto_existente.valor_compra
        tamaho = produto_existente.tamanho
        nova_compra = Compra(
            estoque_id=estoque_id,
            fornecedor_id=fornecedor_id,
            quantidade=quantidade,
            valor_unitario=valor_compra,
            tamanho=tamaho,
            data_compra=datetime.now())
        self.compra_repo.LançamentoCompra(nova_compra, nova_quantidade)
    

    
            


    # def realizar_compra(self, estoque_id: int, fornecedor_id: int, quantidade_comprada: int, valor_unitario: float):
        
    #     print(f"Iniciando processo de compra do produto {estoque_id}...")
