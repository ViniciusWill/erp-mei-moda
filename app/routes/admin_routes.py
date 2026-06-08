from datetime import datetime, timezone

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app.database.usuario_repository import UsuarioRepository
from app.decorators import admin_required, login_required

admin_bp = Blueprint("admin", __name__)

ROLES_VALIDOS = {"admin", "operador"}


@admin_bp.route("/admin/gerenciar-acessos")
@login_required
@admin_required
def gerenciar_acessos():
    repo = UsuarioRepository()
    return render_template(
        "admin/gerenciar_acessos.html",
        usuarios=repo.buscar_todos(),
        emails=repo.buscar_emails_autorizados(),
        usuario_atual_id=session.get("usuario_id"),
    )


@admin_bp.route("/admin/atualizar-role", methods=["POST"])
@login_required
@admin_required
def atualizar_role():
    try:
        usuario_id = int(request.form.get("usuario_id", 0))
        novo_role = request.form.get("role", "").strip()
    except (ValueError, TypeError):
        flash("Requisição inválida.", "error")
        return redirect(url_for("admin.gerenciar_acessos"))

    if novo_role not in ROLES_VALIDOS:
        flash("Tipo de acesso inválido.", "error")
        return redirect(url_for("admin.gerenciar_acessos"))

    if usuario_id == session.get("usuario_id") and novo_role != "admin":
        flash("Você não pode remover seu próprio acesso de administrador.", "error")
        return redirect(url_for("admin.gerenciar_acessos"))

    UsuarioRepository().atualizar_role(usuario_id, novo_role)
    flash("Acesso atualizado com sucesso!", "success")
    return redirect(url_for("admin.gerenciar_acessos"))


@admin_bp.route("/admin/autorizar-email", methods=["POST"])
@login_required
@admin_required
def autorizar_email():
    email = (request.form.get("email") or "").strip().lower()
    if not email or "@" not in email:
        flash("Informe um email válido.", "error")
        return redirect(url_for("admin.gerenciar_acessos"))

    repo = UsuarioRepository()

    if repo.buscar_por_email(email):
        flash(f"O email '{email}' já possui conta cadastrada.", "error")
        return redirect(url_for("admin.gerenciar_acessos"))

    agora = datetime.now(timezone.utc).isoformat(timespec="seconds")
    try:
        repo.autorizar_email(email, agora)
        flash(f"Email '{email}' autorizado com sucesso!", "success")
    except Exception:
        flash(f"O email '{email}' já está na lista de autorizados.", "error")

    return redirect(url_for("admin.gerenciar_acessos"))


@admin_bp.route("/admin/revogar-email", methods=["POST"])
@login_required
@admin_required
def revogar_email():
    try:
        email_id = int(request.form.get("email_id", 0))
    except (ValueError, TypeError):
        flash("Requisição inválida.", "error")
        return redirect(url_for("admin.gerenciar_acessos"))

    UsuarioRepository().revogar_email(email_id)
    flash("Autorização revogada.", "success")
    return redirect(url_for("admin.gerenciar_acessos"))
