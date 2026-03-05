from src.models.Clientes_model import Cliente
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

      