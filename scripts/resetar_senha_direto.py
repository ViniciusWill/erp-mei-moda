import sqlite3
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from werkzeug.security import generate_password_hash


def main():
    caminho = input("Caminho do arquivo .db (Enter para usar o padrão): ").strip()
    if not caminho:
        caminho = str(Path(__file__).resolve().parents[1] / "dados" / "sistema_loja.db")

    if not Path(caminho).exists():
        print(f"Arquivo não encontrado: {caminho}")
        sys.exit(1)

    conn = sqlite3.connect(caminho)
    conn.row_factory = sqlite3.Row

    usuarios = conn.execute("SELECT id, nome, email, cpf FROM usuarios").fetchall()
    if not usuarios:
        print("Nenhum usuário encontrado neste banco.")
        conn.close()
        sys.exit(1)

    print("\nUsuários cadastrados:")
    for u in usuarios:
        print(f"  [{u['id']}] {u['nome']} — {u['email']}")

    usuario_id = input("\nID do usuário para resetar a senha: ").strip()
    usuario = conn.execute("SELECT * FROM usuarios WHERE id = ?", (usuario_id,)).fetchone()

    if not usuario:
        print(f"Usuário com ID {usuario_id} não encontrado.")
        conn.close()
        sys.exit(1)

    nova_senha = input(f"Nova senha para '{usuario['nome']}': ").strip()
    if not nova_senha:
        print("Senha não pode ser vazia.")
        conn.close()
        sys.exit(1)

    novo_hash = generate_password_hash(nova_senha)
    conn.execute("UPDATE usuarios SET senha_hash = ? WHERE id = ?", (novo_hash, usuario_id))
    conn.commit()
    conn.close()

    print(f"\nSenha de '{usuario['nome']}' atualizada com sucesso!")


if __name__ == "__main__":
    main()
