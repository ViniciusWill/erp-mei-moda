from flask import Blueprint, flash, redirect, render_template, url_for

from app.database.Compras_repository import CompraRepository
from app.database.Vendas_repository import VendaRepository

relatorios_bp = Blueprint("relatorios", __name__)


@relatorios_bp.route("/relatorios")
def relatorios():
    compras_repo = CompraRepository()
    vendas_repo = VendaRepository()

    compras = compras_repo.selecionar_todas_compras()
    vendas = vendas_repo.selecionar_todas_vendas()

    total_compras = len(compras)
    total_vendas = len(vendas)
    faturamento_total = sum(v['valor_unitario'] * v['quantidade'] for v in vendas)

    return render_template(
        "relatorios/Relatorios.html",
        logo_header="imagens/Relatorio.png",
        compras=compras,
        vendas=vendas,
        total_compras=total_compras,
        total_vendas=total_vendas,
        faturamento_total=faturamento_total,
    )


@relatorios_bp.route("/relatorios/venda/<int:venda_id>", methods=["POST"])
def excluir_venda(venda_id):
    try:
        VendaRepository().excluir_por_id(venda_id)
        flash("Venda excluída com sucesso!", "sucesso")
    except Exception as exc:
        flash(f"Erro ao excluir venda: {exc}", "erro")
    return redirect(url_for("relatorios.relatorios"))


@relatorios_bp.route("/relatorios/compra/<int:compra_id>", methods=["POST"])
def excluir_compra(compra_id):
    try:
        CompraRepository().excluir_por_id(compra_id)
        flash("Compra excluída com sucesso!", "sucesso")
    except Exception as exc:
        flash(f"Erro ao excluir compra: {exc}", "erro")
    return redirect(url_for("relatorios.relatorios"))