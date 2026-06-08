from functools import wraps
from datetime import datetime, timezone

from flask import flash, redirect, session, url_for


def visitante_ativo():
    expira_em = session.get("visitante_expira_em")
    if not expira_em:
        return False

    try:
        return datetime.fromisoformat(expira_em) > datetime.now(timezone.utc)
    except ValueError:
        return False


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "usuario_id" not in session and not visitante_ativo():
            if session.get("visitante"):
                session.pop("visitante", None)
                session.pop("visitante_inicio", None)
                session.pop("visitante_expira_em", None)
                flash("Seu acesso de visitante expirou. Volte amanha ou entre com um usuario.", "error")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get("usuario_role") != "admin":
            flash("Acesso restrito a administradores.", "error")
            return redirect(url_for("home.index"))
        return f(*args, **kwargs)
    return decorated
