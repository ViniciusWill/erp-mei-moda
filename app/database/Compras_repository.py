from .base_repository import BaseRepository
from app.models.Compras_model import Compra, ContaPagar

class CompraRepository(BaseRepository):
    
    def LançamentoCompra(self, compra: Compra, nova_qtd_estoque: int):
        conn = self._get_connection() 
        try:
            with conn: 
                cur = conn.cursor()
                # -- LANCAMENTO DA COMPRA --
                query_compra = """
                    INSERT INTO compras (estoque_id, fornecedor_id, quantidade, valor_unitario, data_compra) 
                    VALUES (?, ?, ?, ?, ?)
                """
                params_compra = (compra.estoque_id, compra.fornecedor_id, compra.quantidade, compra.valor_unitario, compra.data_compra.strftime("%Y-%m-%d %H:%M:%S"))
                if self.db_url: 
                    query_compra = query_compra.replace("?", "%s")
                    query_compra += " RETURNING id" 
                    
                    cur.execute(query_compra, params_compra)
                    novo_id = cur.fetchone()['id']
                else: 
                    cur.execute(query_compra, params_compra)
                    novo_id = cur.lastrowid
                
                # ---  ATUALIZAR O ESTOQUE ---
                query_estoque = "UPDATE estoque SET quantidade = ? WHERE id = ?"
                if self.db_url:
                    query_estoque = query_estoque.replace("?", "%s")
                
                cur.execute(query_estoque, (nova_qtd_estoque, compra.estoque_id))
                
            return novo_id, compra.valor_unitario
            
        finally:
            conn.close() 


    def LançamentCompraParcelada(self, nova_parcela: ContaPagar):
        query = """
            INSERT INTO contas_a_pagar (compra_id, parcela, valor_parcela, valor_pendente, data_vencimento)
            VALUES (?, ?, ?, ?, ?)
        """
        params = (nova_parcela.compra_id, nova_parcela.parcela, nova_parcela.valor_parcela, nova_parcela.valor_pendente, nova_parcela.data_vencimento)
        self.executar_comando(query, params)


    def buscar_todos_apagar(self):
        query = "SELECT * FROM contas_a_pagar"
        rows = self.executar_select(query)
        return [ContaPagar(**dict(row)) for row in rows]