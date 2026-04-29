from flask import Blueprint, flash, redirect, render_template, request, url_for
import re

from app.database.Participantes_repository import ParticipantesRepository
from app.database.estoque_repository import EstoqueRepository
from app.services.compras_service import CompraService


compras_bp = Blueprint("compras", __name__)


@compras_bp.route("/compras", methods=["GET", "POST"])
def compras():
    estoque_repo = EstoqueRepository()
    participantes_repo = ParticipantesRepository()

    if request.method == "POST":
        try:
            fornecedor_id = int(request.form.get("fornecedor_id"))
            estoque_id = int(request.form.get("estoque_id"))
            quantidade = int(request.form.get("quantidade"))
            parcelas = int(request.form.get("parcelas"))

            service = CompraService()
            id_compra, valor_unitario = service.lancamento_compra(
                fornecedor_id=fornecedor_id,
                estoque_id=estoque_id,
                quantidade=quantidade,
            )

            if parcelas > 1:
                service.lancamento_compra_parcelada(
                    compra_id=id_compra,
                    valor_unitario=valor_unitario,
                    quantidade=quantidade,
                    parcelas=parcelas,
                )

            flash("Compra lançada com sucesso!", "sucesso")
            return redirect(url_for("compras.compras"))
        except Exception as exc:
            flash(f"Erro ao lançar compra: {exc}", "erro")

    produto_selecionado = request.args.get("produto_id", "")
    fornecedor_selecionado = request.args.get("fornecedor_id", "")
    produtos = estoque_repo.buscar_todos()
    participantes = participantes_repo.buscar_todos()
    return render_template(
        "compras/Compra.html",
        logo_header="imagens/compra.png",
        produtos=produtos,
        participantes=participantes,
        produto_selecionado=produto_selecionado,
        fornecedor_selecionado=fornecedor_selecionado,
    )


@compras_bp.route("/compras/novo-produto", methods=["GET", "POST"])
def novo_produto_compra():
    if request.method == "POST":
        try:
            nome = request.form.get("nome", "").strip()
            tamanho = request.form.get("tamanho", "").strip()
            quantidade = int(request.form.get("quantidade", 0))
            valor_unitario = float(request.form.get("valor_unitario", 0))

            estoque_repo = EstoqueRepository()
            novo_id = estoque_repo.inserir_produto(
                nome=nome,
                tamanho=tamanho,
                quantidade=quantidade,
                valor_unitario=valor_unitario,
            )

            flash(f'Produto "{nome}" cadastrado! Agora registre a compra.', "sucesso")
            return redirect(url_for("compras.compras", produto_id=novo_id))
        except Exception as exc:
            flash(f"Erro ao cadastrar produto: {exc}", "erro")

    return render_template(
        "compras/NovoProduto.html",
        logo_header="imagens/compra.png",
    )
@compras_bp.route("/compras/novo-fornecedor", methods=["GET", "POST"])
def novo_fornecedor_compra():
    produto_id = request.args.get("produto_id", "")

    if request.method == "POST":
        try:
            nome = request.form.get("nome", "").strip()
            cnpj = re.sub(r"\D", "", request.form.get("cnpj", ""))

            if len(cnpj) != 14:
                raise ValueError("O CNPJ deve conter exatamente 14 numeros.")

            participantes_repo = ParticipantesRepository()
            novo_id = participantes_repo.inserir_participante(
                nome=nome,
                cnpj=cnpj,
                tipo="fornecedor",
            )

            flash(f'Fornecedor "{nome}" cadastrado! Agora registre a compra.', "sucesso")
            return redirect(
                url_for(
                    "compras.compras",
                    produto_id=produto_id,
                    fornecedor_id=novo_id,
                )
            )
        except Exception as exc:
            flash(f"Erro ao cadastrar fornecedor: {exc}", "erro")

    return render_template(
        "compras/NovoFornecedor.html",
        logo_header="imagens/compra.png",
        produto_id=produto_id,
    )
