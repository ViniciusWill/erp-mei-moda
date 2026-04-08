from .base_repository import BaseRepository
from app.models.Vendas_model import Venda, ContaReceber


class VendaRepository(BaseRepository):

    def lancamento_venda(self, venda: Venda, nova_qtd_estoque: int):
        """Insere a venda e atualiza o estoque em uma única transação."""
        operacoes = [
            (
                """INSERT INTO vendas (cliente_id, estoque_id, quantidade, valor_unitario, data_venda)
                   VALUES (?, ?, ?, ?, ?)""",
                (
                    venda.cliente_id,
                    venda.estoque_id,
                    venda.quantidade,
                    venda.valor_unitario,
                    venda.data_venda.strftime("%Y-%m-%d %H:%M:%S"),
                ),
            ),
            (
                "UPDATE estoque SET quantidade = ? WHERE id = ?",
                (nova_qtd_estoque, venda.estoque_id),
            ),
        ]
        ids = self.executar_transacao(operacoes)
        novo_id = ids[0]
        return novo_id, venda.valor_unitario

    def lancamento_venda_parcelada(self, nova_parcela: ContaReceber):
        self.executar_insert(
            """INSERT INTO contas_a_receber (venda_id, parcela, valor_parcela, valor_pendente, data_vencimento)
               VALUES (?, ?, ?, ?, ?)""",
            (
                nova_parcela.venda_id,
                nova_parcela.parcela,
                nova_parcela.valor_parcela,
                nova_parcela.valor_pendente,
                nova_parcela.data_vencimento,
            ),
        )

    def buscar_todos_areceber(self):
        rows = self.executar_select("SELECT * FROM contas_a_receber")
        return [ContaReceber(**dict(row)) for row in rows]

    def selecionar_todas_vendas(self):
        rows = self.executar_select("SELECT * FROM vendas ORDER BY data_venda DESC")
        return [Venda(**dict(row)) for row in rows]