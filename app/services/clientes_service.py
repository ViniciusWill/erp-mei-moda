from app.database.Clientes_repository import ClienteRepository
from app.models.Clientes_model import Cliente


class ClienteService:
    def __init__(self):
        self.cliente_repo = ClienteRepository()

    def lancamento_cliente(self, nome: str):
        novo_cliente = Cliente(nome=nome)
        self.cliente_repo.salvar(novo_cliente)

    def excluir_cliente(self, cliente_id: int):  
        cliente = self.cliente_repo.buscar_por_id(cliente_id)
        if not cliente:
            raise ValueError("Cliente não encontrado.")
        self.cliente_repo.excluir(cliente)