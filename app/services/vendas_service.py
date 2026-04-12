from datetime import datetime, timedelta

from app.database.Vendas_repository import VendaRepository
from app.database.estoque_repository import EstoqueRepository
from app.models.Vendas_model import ContaReceber, Venda


class VendasService:
    def __init__(self):
        self.venda_repo = VendaRepository()
        self.estoque_repo = EstoqueRepository()

    def realizar_venda(self, cliente_id: int, estoque_id: int, quantidade: int):
        produto = self.estoque_repo.buscar_por_id(estoque_id)
        if not produto:
            raise ValueError("Produto nao encontrado no estoque.")
        if produto.quantidade < quantidade:
            raise ValueError("Estoque insuficiente para realizar a venda.")

        valor_unitario = produto.valor_compra
        nova_quantidade = produto.quantidade - quantidade

        nova_venda = Venda(
            cliente_id=cliente_id,
            estoque_id=estoque_id,
            quantidade=quantidade,
            valor_unitario=valor_unitario,
            data_venda=datetime.now(),
        )
        novo_id_venda, valor_unitario = self.venda_repo.lancamento_venda(
            nova_venda,
            nova_quantidade,
        )
        return novo_id_venda, valor_unitario

    def lancamento_venda_parcelada(
        self,
        venda_id: int,
        valor_unitario: float,
        quantidade: int,
        parcelas: int,
    ):
        valor_total = valor_unitario * quantidade
        valor_parcela = round(valor_total / parcelas, 2)
        data_atual = datetime.now()

        for indice in range(parcelas):
            numero_parcela = indice + 1
            valor_pendente = valor_total - (valor_parcela * indice)
            vencimento = data_atual + timedelta(days=30 * numero_parcela)
            nova_parcela = ContaReceber(
                venda_id=venda_id,
                parcela=numero_parcela,
                valor_parcela=valor_parcela,
                valor_pendente=valor_pendente,
                data_vencimento=vencimento,
            )
            self.venda_repo.lancamento_venda_parcelada(nova_parcela)
