from flask import request, render_template, flash, redirect, url_for, Blueprint
from app.database.Participantes_repository import ParticipantesRepository
from app.database.estoque_repository import EstoqueRepository
from app.services.compras_service import CompraService


compras_bp = Blueprint("compras", __name__)

@compras_bp.route("/compras", methods=["GET", "POST"])
def compras():
        estoque_repo       = EstoqueRepository()
        participantes_repo = ParticipantesRepository()

        if request.method == "POST":
            try:
                fornecedor_id = int(request.form.get("fornecedor_id"))
                estoque_id    = int(request.form.get("estoque_id"))
                quantidade    = int(request.form.get("quantidade"))
                parcelas      = int(request.form.get("parcelas"))

                service = CompraService()
                id_compra, valor_unitario = service.lançamento_compra(
                    fornecedor_id=fornecedor_id,
                    estoque_id=estoque_id,
                    quantidade=quantidade
                )

                if parcelas > 1:
                    service.lançamento_compra_parcelada(
                        compra_id=id_compra,
                        valor_unitario=valor_unitario,
                        quantidade=quantidade,
                        parcelas=parcelas
                    )

                flash("Compra lançada com sucesso!", "sucesso")
                
                return redirect(url_for("compras.compras")) 

            except Exception as e:
                flash(f"Erro ao lançar compra: {str(e)}", "erro")

        produtos      = estoque_repo.buscar_todos()
        participantes = participantes_repo.buscar_todos()

        return render_template("compras/Compra.html",
                               logo_header="imagens/compra.png",
                               produtos=produtos,
                               participantes=participantes)
