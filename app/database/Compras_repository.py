from datetime import datetime
from .base_repository import BaseRepository
from app.models.Compras_model import Compra, ContaPagar


class CompraRepository(BaseRepository):

    def lancamento_compra(self, compra: Compra, nova_qtd_estoque: int):
        """Insere a compra e atualiza o estoque em uma única transação."""
        operacoes = [
            (
                """INSERT INTO compras (estoque_id, fornecedor_id, quantidade, valor_unitario, data_compra)
                   VALUES (?, ?, ?, ?, ?)""",
                (
                    compra.estoque_id,
                    compra.fornecedor_id,
                    compra.quantidade,
                    compra.valor_unitario,
                    compra.data_compra.strftime("%Y-%m-%d %H:%M:%S"),
                ),
            ),
            (
                "UPDATE estoque SET quantidade = ? WHERE id = ?",
                (nova_qtd_estoque, compra.estoque_id),
            ),
        ]
        ids = self.executar_transacao(operacoes)
        novo_id = ids[0]
        return novo_id, compra.valor_unitario

    def lancamento_compra_parcelada(self, nova_parcela: ContaPagar):
        self.executar_insert(
            """INSERT INTO contas_a_pagar (compra_id, parcela, valor_parcela, valor_pendente, data_vencimento)
               VALUES (?, ?, ?, ?, ?)""",
            (
                nova_parcela.compra_id,
                nova_parcela.parcela,
                nova_parcela.valor_parcela,
                nova_parcela.valor_pendente,
                nova_parcela.data_vencimento,
            ),
        )

    def buscar_todos_apagar(self):
        rows = self.executar_select("SELECT * FROM contas_a_pagar")
        return [ContaPagar(**dict(row)) for row in rows]

    def selecionar_todas_compras(self):
        rows = self.executar_select("""
            SELECT 
            compras.id,
            compras.fornecedor_id,
            compras.estoque_id,
            compras.quantidade,
            compras.valor_unitario,
            compras.data_compra,
            estoque.nome_produto,
            estoque.tamanho AS tamanho_produto,
            participantes.nome AS nome_fornecedor
        FROM compras
        JOIN estoque ON compras.estoque_id = estoque.id
        JOIN participantes ON compras.fornecedor_id = participantes.id
    """)
    
        resultado = []
        for row in rows:
            r = dict(row)
        if isinstance(r['data_compra'], str):
            r['data_compra'] = datetime.strptime(r['data_compra'][:10], "%Y-%m-%d")
        resultado.append(r)
        return resultado
    
    def excluir_por_id(self, id: int):
     self.executar_delete("DELETE FROM compras WHERE id = ?", (id,)) 