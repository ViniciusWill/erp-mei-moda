import re

from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.database.Clientes_repository import ClienteRepository
from app.database.estoque_repository import EstoqueRepository
from app.services.vendas_service import VendasService


vendas_bp = Blueprint("vendas", __name__)


@vendas_bp.route("/vendas", methods=["GET", "POST"])
def vendas():
    estoque_repo = EstoqueRepository()
    clientes_repo = ClienteRepository()

    if request.method == "POST":
        try:
            cliente_id = int(request.form.get("cliente_id"))
            estoque_id = int(request.form.get("estoque_id"))
            quantidade = int(request.form.get("Quantidade-ven"))
            parcelas = int(request.form.get("parcelas"))
            service = VendasService()

            id_venda, valor_unitario = service.realizar_venda(
                cliente_id=cliente_id,
                estoque_id=estoque_id,
                quantidade=quantidade,
            )

            if parcelas > 1:
                service.lancamento_venda_parcelada(
                    venda_id=id_venda,
                    valor_unitario=valor_unitario,
                    quantidade=quantidade,
                    parcelas=parcelas,
                )


            flash("Venda lançada com sucesso!", "success")
            return redirect(url_for("home.index"))
        except Exception as exc:
            flash(f"Erro ao lançar venda: {exc}", "error")

    produtos = estoque_repo.buscar_todos()
    clientes = clientes_repo.buscar_todos()
    return render_template(
        "vendas/Venda.html",
        logo_header="imagens/venda.png",
        produtos=produtos,
        clientes=clientes,
    )


@vendas_bp.route("/vendas/novo-cliente", methods=["GET", "POST"])
def novo_cliente_venda():
    if request.method == "POST":
        try:
            nome = request.form.get("nome", "").strip()
            cpf = re.sub(r"\D", "", request.form.get("cpf", ""))

            if not nome:
                flash("Nome e obrigatorio.", "erro")
                return redirect(url_for("vendas.novo_cliente_venda"))

            if len(cpf) != 11:
                flash("O CPF deve conter exatamente 11 numeros.", "error")
                return redirect(url_for("vendas.novo_cliente_venda"))

            cliente_repo = ClienteRepository()
            cliente_repo.inserir_cliente(nome=nome, cpf=cpf)

            flash("Cliente cadastrado com sucesso!", "success")
            return redirect(url_for("home.index"))
        except Exception as exc:
            flash(f"Erro ao cadastrar cliente: {exc}", "error")

    return render_template(
        "vendas/NovoCliente.html",
        logo_header="imagens/venda.png",
    )
