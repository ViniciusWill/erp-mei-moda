import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.database.usuario_repository import UsuarioRepository


def main():
    nome = input("Nome do usuário: ").strip()
    email = input("Email: ").strip()
    cpf = input("CPF: ").strip()
    cnpj = input("CNPJ (opcional): ").strip()
    senha = input("Senha: ").strip()

    if not nome or not senha or not email:
        print("Erro: nome, email e senha não podem ser vazios.")
        sys.exit(1)

    repo = UsuarioRepository()
    repo.criar_usuario(nome, email, cpf, cnpj, senha)
    print(f"Usuário '{nome}' criado com sucesso!")


if __name__ == "__main__":
    main()