from app.models.Clientes_model import Cliente
from .base_repository import BaseRepository

class ClienteRepository(BaseRepository):
    
    def salvar(self, cliente: Cliente):
        conn = self.__conection__()
        
        try:
            with conn: 
                cur = conn.cursor()
                query = "INSERT INTO clientes (nome) VALUES (?)"
                
                if self.db_url:
                    query = query.replace("?", "%s")
                    
                cur.execute(query, (cliente.nome,))
                
        finally:
            conn.close()

    def buscar_todos(self):
        conn = self.__conection__()
        try:
            cur = conn.cursor()
            query = "SELECT * FROM clientes"
            cur.execute(query)
            rows = cur.fetchall()
            return [{"id": row["id"], "nome": row["nome"]} for row in rows]
        finally:
            conn.close()