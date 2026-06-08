import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.database.usuario_repository import UsuarioRepository


def main():
    repo = UsuarioRepository()

    identificador = input("Nome, email ou CPF do usuário: ").strip()
    usuario = repo.buscar_por_identificador(identificador)

    if not usuario:
        print(f"Usuário '{identificador}' não encontrado.")
        sys.exit(1)

    print(f"Usuário encontrado: {usuario.nome} ({usuario.email})")

    nova_senha = input("Nova senha: ").strip()
    if not nova_senha:
        print("Erro: senha não pode ser vazia.")
        sys.exit(1)

    repo.atualizar_senha_hash(usuario.id, nova_senha)
    print(f"Senha do usuário '{usuario.nome}' atualizada com sucesso!")


if __name__ == "__main__":
    main()
