from datetime import datetime, timedelta
from app.models.Vendas_model import Venda, ContaReceber
from app.database.Vendas_repository import VendaRepository
from app.database.estoque_repository import EstoqueRepository

class VendasService:
    def __init__(self):
        self.venda_repo = VendaRepository()
        self.estoque_repo = EstoqueRepository()

    def realizar_venda(self, cliente_id: int, estoque_id: int, quantidade: int):
        produto = self.estoque_repo.buscar_por_id(estoque_id)
        if not produto:
            raise ValueError("Erro: Produto não encontrado no estoque!")
        if produto.quantidade < quantidade:
            raise ValueError(f"Estoque insuficiente!")
        valor_unitario = produto.valor_compra  
        nova_quantidade = produto.quantidade - quantidade

        nova_venda = Venda(
        cliente_id=cliente_id,
        estoque_id=estoque_id,
        quantidade=quantidade,
        valor_unitario=valor_unitario,
        data_venda=datetime.now()
    )
        novo_id_venda = self.venda_repo.LançamentoVenda(nova_venda, nova_quantidade)
        return novo_id_venda, valor_unitario
    
    def lançamento_venda_parcelada(self, venda_id: int, valor_unitario: float, quantidade: int, parcelas: int):
        valor_total = valor_unitario * quantidade
        valor_parcelas = round(valor_total / parcelas, 2)
        data_atual = datetime.now() 
        for i in range(parcelas):
            numero_parcela = i + 1 
            total_atualizado = valor_total - (valor_parcelas * i)
            dias_para_frente = 30 * numero_parcela
            vencimento = data_atual + timedelta(days=dias_para_frente)
            nova_parcela = ContaReceber(
            venda_id=venda_id,
            parcela = numero_parcela,
            valor_parcela = valor_parcelas,
            valor_pendente=total_atualizado,
            data_vencimento =vencimento
            )
            self.venda_repo.LançamentoVendaParcelada(nova_parcela)
