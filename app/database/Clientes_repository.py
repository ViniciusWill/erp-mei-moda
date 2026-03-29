from app.models.Clientes_model import Cliente
from .base_repository import BaseRepository

class ClienteRepository(BaseRepository):
    def salvar(self, cliente: Cliente):
        with self.__conection__() as conn: 
            try:
                cur = conn.cursor()
                cur.execute("""INSERT INTO clientes (nome) VALUES (?)""", (cliente.nome,))
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise e
    def buscar_todos(self):
        with self.__conection__() as conn:
           cur = conn.cursor()
           cur.execute("SELECT * FROM clientes")
           rows = cur.fetchall()
        return [{"id": row["id"], "nome": row["nome"]} for row in rows]


      