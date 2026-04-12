from datetime import datetime

from flask import Blueprint, render_template

from app.database.Vendas_repository import VendaRepository


contas_a_receber_bp = Blueprint("contas_a_receber", __name__)


@contas_a_receber_bp.route("/financeiro/contas_receber")
def contas_receber():
    repo = VendaRepository()
    contas = repo.buscar_todos_areceber()
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
        "financeiro/ContasReceber.html",
        logo_header="imagens/receber.png",
        contas=contas,
        hoje=hoje,
        total_contas=total_contas,
        total_pendente=total_pendente,
        total_vencidas=total_vencidas,
    )
