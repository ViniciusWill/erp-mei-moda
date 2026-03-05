from src.database.Clientes_repository import ClienteRepository
from src.models.Clientes_model import Cliente


class ClienteService:
    def __init__(self):
        self.cliente_repo = ClienteRepository()

    def LançamentoClienteCamposObrigatorios(self, nome: str):
        try:    
            novo_cliente = Cliente(nome=nome)
            self.cliente_repo.salvar(novo_cliente)
        except Exception as e: 
           raise e
            