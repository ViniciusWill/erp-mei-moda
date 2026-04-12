from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.database.Participantes_repository import ParticipantesRepository
from app.services.participantes_service import ParticipanteService


participantes_bp = Blueprint("participantes", __name__)


@participantes_bp.route("/participantes", methods=["GET", "POST"])
def participantes():
    if request.method == "POST":
        try:
            nome = request.form.get("nome", "").strip()
            ParticipanteService().lancamento_participante(nome=nome)
            flash("Participante cadastrado com sucesso!", "sucesso")
            return redirect(url_for("participantes.participantes"))
        except Exception as exc:
            flash(f"Erro ao cadastrar participante: {exc}", "erro")

    participantes_repo = ParticipantesRepository()
    partic = participantes_repo.buscar_todos()
    total_partic = len(partic)
    return render_template(
        "participantes/Participantes.html",
        logo_header="imagens/participantes.png",
        partic=partic,
        total_partic=total_partic,
    )


@participantes_bp.route("/participantes/<int:participante_id>", methods=["POST"])
def excluir_participante(participante_id):
    try:
        ParticipanteService().excluir_participante(participante_id)
        flash("Participante excluído com sucesso!", "sucesso")
    except Exception as exc:
        erro = str(exc)
        if "foreign key" in erro.lower() or "fkey" in erro.lower():
            flash(
                "Este participante possui compras registradas. "
                "Para excluí-lo, primeiro exclua as compras vinculadas a ele na tela de Relatórios.",
                "erro"
            )
        else:
            flash(f"Erro ao excluir participante: {exc}", "erro")
    return redirect(url_for("participantes.participantes"))