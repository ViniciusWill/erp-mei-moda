from datetime import datetime, timedelta

from app.database.Compras_repository import CompraRepository
from app.database.estoque_repository import EstoqueRepository
from app.models.Compras_model import Compra, ContaPagar


class CompraService:
    def __init__(self):
        self.compra_repo = CompraRepository()
        self.estoque_repo = EstoqueRepository()

    def lancamento_compra(self, fornecedor_id: int, estoque_id: int, quantidade: int):
        produto = self.estoque_repo.buscar_por_id(estoque_id)
        if not produto:
            raise ValueError("Produto nao encontrado no estoque.")

        nova_quantidade = produto.quantidade + quantidade
        valor_compra = produto.valor_compra

        nova_compra = Compra(
            estoque_id=estoque_id,
            fornecedor_id=fornecedor_id,
            quantidade=quantidade,
            valor_unitario=valor_compra,
            data_compra=datetime.now(),
        )
        id_compra, valor_unitario = self.compra_repo.lancamento_compra(
            nova_compra,
            nova_quantidade,
        )
        return id_compra, valor_unitario

    def lancamento_compra_parcelada(
        self,
        compra_id: int,
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
            nova_parcela = ContaPagar(
                compra_id=compra_id,
                parcela=numero_parcela,
                valor_parcela=valor_parcela,
                valor_pendente=valor_pendente,
                data_vencimento=vencimento,
            )
            self.compra_repo.lancamento_compra_parcelada(nova_parcela)
