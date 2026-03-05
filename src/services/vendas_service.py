from datetime import datetime
from src.models.Vendas_model import Venda
from src.database.Vendas_repository import VendaRepository
from src.database.estoque_repository import EstoqueRepository

class VendasService:
    def __init__(self):
        self.venda_repo = VendaRepository()
        self.estoque_repo = EstoqueRepository()

    def realizar_venda(self, cliente_id: int, estoque_id: int, quantidade_desejada: int, valor_unitario: float):
     
        print(f"Iniciando processo de venda do produto {estoque_id}...")

        produto = self.estoque_repo.buscar_por_id(estoque_id)
        if not produto:
            raise ValueError("Erro: Produto não encontrado no estoque!")

        if produto.quantidade < quantidade_desejada:
            raise ValueError(f"Estoque insuficiente! Temos apenas {produto.quantidade} unidades de '{produto.nome_produto}'.")

        nova_quantidade = produto.quantidade - quantidade_desejada

        # 4. Criar o Modelo (O Pydantic valida os dados aqui)
        nova_venda = Venda(
            cliente_id=cliente_id,
            estoque_id=estoque_id,
            quantidade=quantidade_desejada,
            valor_unitario=valor_unitario,
            data_venda=datetime.now()
        )

        self.venda_repo.LançamentoVenda(nova_venda, nova_quantidade)
        
        print(f"Sucesso! Venda de {quantidade_desejada}x '{produto.nome_produto}' finalizada.")
        return nova_venda