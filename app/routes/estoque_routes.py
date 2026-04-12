from flask import Blueprint, render_template

from app.database.estoque_repository import EstoqueRepository


estoque_bp = Blueprint("estoque", __name__)


@estoque_bp.route("/estoque")
def estoque():
    estoque_repo = EstoqueRepository()
    produtos = estoque_repo.buscar_todos()

    total_itens = len(produtos)
    estoque_baixo = sum(1 for produto in produtos if 0 < produto.quantidade <= 5)
    estoque_zerado = sum(1 for produto in produtos if produto.quantidade <= 0)

    return render_template(
        "estoque/Estoque.html",
        logo_header="imagens/estoque.png",
        produtos=produtos,
        total_itens=total_itens,
        estoque_baixo=estoque_baixo,
        estoque_zerado=estoque_zerado,
    )
