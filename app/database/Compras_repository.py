from .base_repository import BaseRepository
from app.models.Compras_model import Compra, ContaPagar

class CompraRepository(BaseRepository):
    def LançamentoCompra(self, compra: Compra, nova_qtd_estoque: int):
        with self.__conection__() as conn:
            try: 
                cur = conn.cursor()
                cur.execute("""  
                            INSERT INTO compras (estoque_id, fornecedor_id, quantidade, valor_unitario, data_compra) 
                            VALUES (?, ?, ?, ?, ?)
                            """, (compra.estoque_id, compra.fornecedor_id, compra.quantidade, compra.valor_unitario, compra.data_compra.strftime("%Y-%m-%d %H:%M:%S")))
                cur.execute("UPDATE estoque SET quantidade = ? WHERE id = ?", 
                               (nova_qtd_estoque, compra.estoque_id))
                
                novo_id = cur.lastrowid
                conn.commit()
                return novo_id, compra.valor_unitario
            except Exception as e:
                conn.rollback()
                raise e
    def LançamentCompraParcelada(self, nova_parcela: ContaPagar):
        with self.__conection__() as conn:
            try:
                cur = conn.cursor()
                cur.execute(""" INSERT INTO contas_a_pagar (compra_id, parcela, valor_parcela, valor_pendente, data_vencimento)
                             VALUES  (? , ?, ?, ?, ?) """,
                               (nova_parcela.compra_id, nova_parcela.parcela, nova_parcela.valor_parcela, nova_parcela.valor_pendente, nova_parcela.data_vencimento ))
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise e
            