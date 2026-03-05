from .base_repository import BaseRepository
from src.models import Venda

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
            except Exception as e:
                conn.rollback()
                raise e