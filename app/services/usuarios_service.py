from app.database.usuario_repository import UsuarioRepository


class UsuarioService:
    def __init__(self):
        self.usuario_repo = UsuarioRepository()

    def cadastrar_usuario(self, nome: str, email: str, cpf: str, cnpj: str, senha: str, confirmar_senha: str):
        nome = (nome or "").strip()
        email = (email or "").strip().lower()
        cpf = (cpf or "").strip()
        cnpj = (cnpj or "").strip()
        senha = (senha or "").strip()
        confirmar_senha = (confirmar_senha or "").strip()

        if not nome:
            raise ValueError("Informe o nome do usuario.")
        if not email:
            raise ValueError("Informe o email do usuario.")
        if not cpf:
            raise ValueError("Informe o CPF do usuario.")
        if len(senha) < 6:
            raise ValueError("A senha precisa ter pelo menos 6 caracteres.")
        if senha != confirmar_senha:
            raise ValueError("As senhas informadas nao conferem.")

        if not self.usuario_repo.email_esta_autorizado(email):
            raise ValueError("Este email nao foi autorizado pelo administrador. Solicite acesso ao responsavel.")

        if self.usuario_repo.buscar_por_nome(nome):
            raise ValueError("Ja existe um usuario cadastrado com esse nome.")
        if self.usuario_repo.buscar_por_email(email):
            raise ValueError("Ja existe um usuario cadastrado com esse email.")
        if self.usuario_repo.buscar_por_cpf(cpf):
            raise ValueError("Ja existe um usuario cadastrado com esse CPF.")

        resultado = self.usuario_repo.criar_usuario(nome, email, cpf, cnpj, senha)
        self.usuario_repo.marcar_email_usado(email)
        return resultado
