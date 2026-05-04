from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.database.Clientes_repository import ClienteRepository
from app.services.clientes_service import ClienteService


clientes_bp = Blueprint("clientes", __name__)


@clientes_bp.route("/clientes", methods=["GET"])
def clientes():
    clientes_repo = ClienteRepository()
    cli = clientes_repo.buscar_todos()
    total_cli = len(cli)
    return render_template(
        "clientes/Clientes.html",
        logo_header="imagens/Clientes.png",
        cli=cli,
        total_cli=total_cli,
    )


@clientes_bp.route("/clientes/novo", methods=["GET", "POST"])
def novo_cliente():
    if request.method == "POST":
        try:
            nome = request.form.get("nome", "").strip()
            cpf = request.form.get("cpf", "").strip()
            ClienteService().lancamento_cliente(nome=nome, cpf=cpf)
            flash("Cliente cadastrado com sucesso!", "success")
            return redirect(url_for("clientes.clientes"))
        except Exception as exc:
            flash(f"Erro ao cadastrar cliente: {exc}", "error")

    return render_template(
        "clientes/NovoCliente.html",
        logo_header="imagens/Clientes.png",
    )

@clientes_bp.route("/clientes/<int:cliente_id>", methods=["POST"])
def excluir_cliente(cliente_id):
    try:
        ClienteService().excluir_cliente(cliente_id)
        flash("Cliente excluído com sucesso!", "success")
    except Exception as exc:
        erro = str(exc)
        if "foreign key" in erro.lower() or "fkey" in erro.lower():
            flash(
                "Este cliente possui vendas registradas. "
                "Para excluí-lo, primeiro exclua as vendas vinculadas a ele na tela de Relatórios.",
                "erro"
            )
        else:
            flash(f"Erro ao excluir cliente: {exc}", "error")
    return redirect(url_for("clientes.clientes"))
