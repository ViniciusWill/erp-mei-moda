from flask import Blueprint, render_template, session

from app.decorators import login_required

home_bp = Blueprint("home", __name__)


@home_bp.route("/")
@login_required
def index():
    is_admin = session.get("usuario_role") == "admin"
    return render_template("index.html", logo_header="imagens/logo.ico", is_admin=is_admin)
