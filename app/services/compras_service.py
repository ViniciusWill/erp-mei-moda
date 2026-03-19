from datetime import datetime, timedelta
from app.models.Compras_model import Compra, ContaPagar
from app.database.Compras_repository import CompraRepository
from app.database.estoque_repository import EstoqueRepository

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
        id_nova_compra, valor_nova_compra = self.compra_repo.LançamentoCompra(nova_compra, nova_quantidade)
        return id_nova_compra, valor_nova_compra
        

    def lançamento_compra_parcelada(self, compra_id: int, valor_unitario: float, quantidade: int, parcelas: int):
        valor_total = valor_unitario * quantidade
        valor_parcelas = round(valor_total / parcelas, 2)
        data_atual = datetime.now() 
        for i in range(parcelas):
            numero_parcela = i + 1 
            total_atualizado = valor_total - (valor_parcelas * i)
            dias_para_frente = 30 * numero_parcela
            vencimento = data_atual + timedelta(days=dias_para_frente)
            nova_parcela = ContaPagar(
            compra_id=compra_id,
            parcela = numero_parcela,
            valor_parcela = valor_parcelas,
            valor_pendente=total_atualizado,
            data_vencimento =vencimento
            )
            self.compra_repo.LançamentCompraParcelada(nova_parcela)


    
