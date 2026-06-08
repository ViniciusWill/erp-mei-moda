import secrets
from datetime import datetime, timedelta, timezone

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from app.database.usuario_repository import UsuarioRepository
from app.services.email_service import EmailConfigError, enviar_email_recuperacao
from app.services.usuarios_service import UsuarioService

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        identificador = (
            request.form.get("nome")
            or request.form.get("username")
            or request.form.get("email")
            or ""
        ).strip()
        senha = (
            request.form.get("senha")
            or request.form.get("password")
            or ""
        ).strip()

        if not identificador or not senha:
            flash("Informe usuario e senha para continuar.", "error")
            return render_template("auth/login.html", logo_header="favicon.ico")

        repo = UsuarioRepository()
        usuario = repo.buscar_por_identificador(identificador)

        if repo.verificar_senha(usuario, senha):
            session.pop("visitante", None)
            session.pop("visitante_inicio", None)
            session.pop("visitante_expira_em", None)
            session["usuario_id"] = usuario.id
            session["usuario_role"] = usuario.role
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for("home.index"))
        else:
            flash("Nome ou senha incorretos.", "error")

    return render_template("auth/login.html", logo_header="favicon.ico")

@auth_bp.route("/logout")
def logout(): 
    session.pop("usuario_id", None)
    session.pop("visitante", None)
    session.pop("visitante_inicio", None)
    session.pop("visitante_expira_em", None)
    flash("Logout realizado com sucesso!", "success")
    return redirect(url_for("auth.login"))


@auth_bp.route("/auth/visitante")
def visitante():
    from app.database.db_config import visitor_engine
    from app.database.orm_models import Base as OrmBase

    # Banco do visitante sempre zerado a cada novo acesso
    OrmBase.metadata.drop_all(visitor_engine)
    OrmBase.metadata.create_all(visitor_engine)

    agora = datetime.now(timezone.utc)
    expira_em = agora + timedelta(hours=1)

    session.pop("usuario_id", None)
    session.pop("usuario_role", None)
    session["visitante"] = True
    session["visitante_inicio"] = agora.isoformat(timespec="seconds")
    session["visitante_expira_em"] = expira_em.isoformat(timespec="seconds")
    flash("Acesso visitante liberado. Banco de demonstracao zerado e pronto.", "success")
    return redirect(url_for("home.index"))


@auth_bp.route("/auth/cadastrar-cliente", methods=["GET", "POST"])
def cadastrar_cliente():
    if request.method == "POST":
        try:
            nome = request.form.get("nome", "").strip()
            email = request.form.get("email", "").strip()
            cpf = request.form.get("cpf", "").strip()
            cnpj = request.form.get("cnpj", "").strip()
            senha = request.form.get("senha", "").strip()
            confirmar_senha = request.form.get("confirmar_senha", "").strip()
            UsuarioService().cadastrar_usuario(
                nome=nome,
                email=email,
                cpf=cpf,
                cnpj=cnpj,
                senha=senha,
                confirmar_senha=confirmar_senha,
            )
            flash("Usuario cadastrado com sucesso. Entre com suas credenciais.", "success")
            return redirect(url_for("auth.login"))
        except ValueError as exc:
            flash(str(exc), "error")
        except Exception as exc:
            flash(f"Erro ao cadastrar usuario: {exc}", "error")

    return render_template("auth/cadastrar_cliente.html", logo_header="favicon.ico")


@auth_bp.route("/auth/esquecisenha", methods=["GET", "POST"])
def esquecisenha():
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        repo = UsuarioRepository()
        usuario = repo.buscar_por_email(email)

        if not usuario:
            flash("Se o email estiver cadastrado, voce recebera um codigo de recuperacao.", "info")
            return redirect(url_for("auth.verificar_codigo", email=email))

        codigo = f"{secrets.randbelow(1_000_000):06d}"
        repo.salvar_codigo_recuperacao(usuario.id, codigo)

        try:
            enviar_email_recuperacao(usuario.email, codigo)
        except EmailConfigError as erro:
            repo.marcar_codigos_recuperacao_usados(usuario.id)
            flash(str(erro), "error")
            return redirect(url_for("auth.esquecisenha"))
        except Exception:
            repo.marcar_codigos_recuperacao_usados(usuario.id)
            flash("Nao foi possivel enviar o email agora. Verifique a configuracao SMTP.", "error")
            return redirect(url_for("auth.esquecisenha"))

        flash("Enviamos um codigo de recuperacao para o email informado.", "success")
        return redirect(url_for("auth.verificar_codigo", email=email))

    return render_template("auth/esquecisenha.html", logo_header="favicon.ico")


@auth_bp.route("/auth/verificar-codigo", methods=["GET", "POST"])
def verificar_codigo():
    email = (request.values.get("email") or "").strip().lower()

    if request.method == "POST":
        codigo = (request.form.get("codigo") or "").strip()
        repo = UsuarioRepository()
        usuario = repo.buscar_por_email(email)

        if usuario and repo.validar_codigo_recuperacao(usuario.id, codigo):
            session["reset_usuario_id"] = usuario.id
            flash("Codigo confirmado. Cadastre sua nova senha.", "success")
            return redirect(url_for("auth.nova_senha"))

        flash("Codigo invalido ou expirado.", "error")

    return render_template("auth/verificar_codigo.html", email=email, logo_header="favicon.ico")


@auth_bp.route("/auth/nova-senha", methods=["GET", "POST"])
def nova_senha():
    usuario_id = session.get("reset_usuario_id")
    if not usuario_id:
        flash("Solicite um codigo de recuperacao para alterar sua senha.", "error")
        return redirect(url_for("auth.esquecisenha"))

    if request.method == "POST":
        senha = (request.form.get("senha") or "").strip()
        confirmar_senha = (request.form.get("confirmar_senha") or "").strip()

        if len(senha) < 6:
            flash("A nova senha precisa ter pelo menos 6 caracteres.", "error")
            return render_template("auth/nova_senha.html", logo_header="favicon.ico")

        if senha != confirmar_senha:
            flash("As senhas informadas nao conferem.", "error")
            return render_template("auth/nova_senha.html", logo_header="favicon.ico")

        repo = UsuarioRepository()
        repo.atualizar_senha_hash(usuario_id, senha)
        repo.marcar_codigos_recuperacao_usados(usuario_id)
        session.pop("reset_usuario_id", None)
        flash("Senha atualizada com sucesso. Entre com sua nova senha.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/nova_senha.html", logo_header="favicon.ico")
