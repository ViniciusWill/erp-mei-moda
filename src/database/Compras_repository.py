from .base_repository import BaseRepository
from src.models.Compras_model import Compra

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
                
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise e