from flask import Blueprint, request, render_template, flash
from app.database.estoque_repository import EstoqueRepository
from app.database.Clientes_repository import ClienteRepository
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
                quantidade=quantidade
            )
        
                if parcelas > 1:
                    service.lançamento_venda_parcelada(
                        venda_id=id_venda,
                        valor_unitario=valor_unitario,
                        quantidade=quantidade,
                        parcelas=parcelas
                    )

          

            except Exception as e:
                flash(f"Erro ao lançar venda: {str(e)}", "erro")
        
    produtos      = estoque_repo.buscar_todos()
    clientes      = clientes_repo.buscar_todos()
    return render_template("vendas/Venda.html", logo_header="imagens/venda.png", produtos=produtos, clientes=clientes)
