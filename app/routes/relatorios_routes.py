from flask import render_template, Blueprint
from app.database.Compras_repository import CompraRepository
from app.database.Vendas_repository import VendaRepository

relatorios_bp = Blueprint("relatorios", __name__)
@relatorios_bp.route("/relatorios")
def relatorios():
    compras_repo = CompraRepository()
    vendas_repo = VendaRepository()

    total_compras = compras_repo.selecionar_todas_compras()
    total_vendas = vendas_repo.selecionar_todas_vendas()

    return render_template(
        "Relatorios/Relatorios.html",
        logo_header="imagens/Relatorio.png",
        total_compras=total_compras,
        total_vendas=total_vendas
    )