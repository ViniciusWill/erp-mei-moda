from flask import request, render_template, flash, redirect, url_for, Blueprint
from app.database.Clientes_repository import ClienteRepository
from app.services.clientes_service import ClienteService



clientes_bp = Blueprint("clientes", __name__)

@clientes_bp.route("/clientes", methods=["GET", "POST"]) 
def clientes():
  
        if request.method == "POST":
            try:
                nome = request.form.get("nome")
                service = ClienteService()
                service.LançamentoClienteCamposObrigatorios(nome=nome)
                flash("Cliente cadastrado com sucesso!", "sucesso")
                return redirect(url_for("clientes.clientes"))
            except  Exception as e:
                flash(f"Erro ao cadastrar cliente: {str(e)}", "erro")

        clientes_repo = ClienteRepository()
        cli = clientes_repo.buscar_todos()
        total_cli = len(cli)
        return render_template("clientes/Clientes.html",
                               logo_header="imagens/Clientes.png",
                               cli=cli,
                               total_cli=total_cli)
