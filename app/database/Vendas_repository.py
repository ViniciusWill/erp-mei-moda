from .base_repository import BaseRepository
from app.models.Vendas_model import Venda, ContaReceber 

class VendaRepository(BaseRepository):
    
    def LançamentoVenda(self, venda: Venda, nova_qtd_estoque: int):
        conn = self._get_connection()
        try:
            with conn:
                cur = conn.cursor()
                
                # --- 1. INSERIR A VENDA E PEGAR O ID ---
                query_venda = """
                    INSERT INTO vendas (cliente_id, estoque_id, quantidade, valor_unitario, data_venda)
                    VALUES (?, ?, ?, ?, ?)
                """
                params_venda = (venda.cliente_id, venda.estoque_id, venda.quantidade, 
                                venda.valor_unitario, venda.data_venda.strftime("%Y-%m-%d %H:%M:%S"))
                
    
                if self.db_url:
                    query_venda = query_venda.replace("?", "%s")
                    query_venda += " RETURNING id"
                    cur.execute(query_venda, params_venda)
                    novo_id_venda = cur.fetchone()['id']
                else:
                    cur.execute(query_venda, params_venda)
                    novo_id_venda = cur.lastrowid 
                
                # --- 2. DAR BAIXA NO ESTOQUE ---
                query_estoque = "UPDATE estoque SET quantidade = ? WHERE id = ?"
                if self.db_url:
                    query_estoque = query_estoque.replace("?", "%s")
                    
                cur.execute(query_estoque, (nova_qtd_estoque, venda.estoque_id))
                
                return novo_id_venda
                
        finally:
            conn.close() 

    def LançamentoVendaParcelada(self, nova_parcela: ContaReceber):
        """Salva uma nova parcela de conta a receber no banco."""
        query = """
            INSERT INTO contas_a_receber (venda_id, parcela, valor_parcela, valor_pendente, data_vencimento)
            VALUES (?, ?, ?, ?, ?)
        """
        params = (nova_parcela.venda_id, nova_parcela.parcela, nova_parcela.valor_parcela, 
                  nova_parcela.valor_pendente, nova_parcela.data_vencimento)
                  
        self.executar_comando(query, params)

    def buscar_todos_areceber(self):
        """Retorna todas as contas a receber do sistema."""
        query = "SELECT * FROM contas_a_receber"
        rows = self.executar_select(query)
        
        return [ContaReceber(**dict(row)) for row in rows]