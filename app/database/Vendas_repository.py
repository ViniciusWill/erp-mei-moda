from .base_repository import BaseRepository
from app.models.Vendas_model import Venda, ContaReceber 

class VendaRepository(BaseRepository):
    def LançamentoVenda(self, venda: Venda, nova_qtd_estoque: int):
        with self.__conection__() as conn:
            try:
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO vendas (cliente_id, estoque_id, quantidade, valor_unitario, data_venda)
                    VALUES (?, ?, ?, ?, ?)
                """, (venda.cliente_id, venda.estoque_id, venda.quantidade, 
                      venda.valor_unitario, venda.data_venda.strftime("%Y-%m-%d %H:%M:%S")))

                cur.execute("UPDATE estoque SET quantidade = ? WHERE id = ?", 
                               (nova_qtd_estoque, venda.estoque_id))
                
                conn.commit()
                novo_id_venda = cur.lastrowid
                return novo_id_venda
            except Exception as e:
                conn.rollback()
                raise e
    def LançamentoVendaParcelada(self, nova_parcela: ContaReceber):
        with self.__conection__() as conn:
            try:
                cur = conn.cursor()
                cur.execute(""" INSERT INTO contas_a_receber (venda_id, parcela, valor_parcela, valor_pendente, data_vencimento)
                             VALUES  (? , ?, ?, ?, ?) """,
                               (nova_parcela.venda_id, nova_parcela.parcela, nova_parcela.valor_parcela, nova_parcela.valor_pendente, nova_parcela.data_vencimento ))
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise e
    def buscar_todos_areceber(self):
        with self.__conection__() as conn:
           cur = conn.cursor()
           cur.execute("SELECT * FROM contas_a_receber")
           rows = cur.fetchall()
        return [ContaReceber(**dict(row)) for row in rows]
        
            