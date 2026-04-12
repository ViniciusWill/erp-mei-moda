from datetime import datetime

from flask import Blueprint, render_template

from app.database.Compras_repository import CompraRepository


contas_a_pagar_bp = Blueprint("contas_a_pagar", __name__)


@contas_a_pagar_bp.route("/financeiro/contas_pagar")
def contas_pagar():
    repo = CompraRepository()
    contas = repo.buscar_todos_apagar()
    hoje = datetime.now()

    for conta in contas:
        if conta.data_vencimento.tzinfo is not None:
            conta.data_vencimento = conta.data_vencimento.replace(tzinfo=None)

    total_contas = len(contas)
    total_pendente = sum(conta.valor_pendente for conta in contas if conta.valor_pendente > 0)
    total_vencidas = sum(
        1 for conta in contas if conta.valor_pendente > 0 and conta.data_vencimento < hoje
    )

    return render_template(
        "financeiro/ContasPagar.html",
        logo_header="imagens/pagar.png",
        contas=contas,
        hoje=hoje,
        total_contas=total_contas,
        total_pendente=total_pendente,
        total_vencidas=total_vencidas,
    )
