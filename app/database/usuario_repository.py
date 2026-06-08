from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from werkzeug.security import check_password_hash, generate_password_hash

from app.database.base_repository import BaseRepository
from app.database.orm_models import EmailAutorizado as EmailAutorizadoORM
from app.database.orm_models import RecuperacaoSenha as RecuperacaoSenhaORM
from app.database.orm_models import Usuario as UsuarioORM
from app.models.Usuario_model import Usuario


class UsuarioRepository(BaseRepository):

    def _to_usuario(self, row: UsuarioORM | None) -> Usuario | None:
        if not row:
            return None
        return Usuario(
            id=row.id,
            nome=row.nome,
            cpf=row.cpf,
            cnpj=row.cnpj if row.cnpj != "" else None,
            email=row.email,
            senha_hash=row.senha_hash,
            role=row.role or "operador",
        )

    def buscar_todos(self) -> list[Usuario]:
        with self._session() as session:
            rows = session.execute(select(UsuarioORM)).scalars().all()
            return [self._to_usuario(r) for r in rows]

    def atualizar_role(self, usuario_id: int, role: str):
        with self._session() as session:
            usuario = session.get(UsuarioORM, usuario_id)
            if usuario:
                usuario.role = role

    def criar_usuario(self, nome: str, email: str, cpf: str, cnpj: str, senha: str):
        senha_hash = generate_password_hash(senha)
        with self._session() as session:
            novo = UsuarioORM(nome=nome, email=email, cpf=cpf, cnpj=cnpj, senha_hash=senha_hash)
            session.add(novo)

    def buscar_por_id(self, usuario_id: int) -> Usuario | None:
        with self._session() as session:
            row = session.get(UsuarioORM, usuario_id)
            return self._to_usuario(row)

    def buscar_por_nome(self, nome: str) -> Usuario | None:
        with self._session() as session:
            from sqlalchemy import func
            stmt = select(UsuarioORM).where(func.lower(UsuarioORM.nome) == nome.lower())
            row = session.execute(stmt).scalar_one_or_none()
            return self._to_usuario(row)

    def buscar_por_identificador(self, identificador: str) -> Usuario | None:
        with self._session() as session:
            stmt = select(UsuarioORM).where(
                (UsuarioORM.nome == identificador)
                | (UsuarioORM.email == identificador)
                | (UsuarioORM.cpf == identificador)
            )
            row = session.execute(stmt).scalar_one_or_none()
            return self._to_usuario(row)

    def buscar_por_cpf(self, cpf: str) -> Usuario | None:
        with self._session() as session:
            stmt = select(UsuarioORM).where(UsuarioORM.cpf == cpf)
            row = session.execute(stmt).scalar_one_or_none()
            return self._to_usuario(row)

    def buscar_por_email(self, email: str) -> Usuario | None:
        with self._session() as session:
            from sqlalchemy import func
            stmt = select(UsuarioORM).where(func.lower(UsuarioORM.email) == email.lower())
            row = session.execute(stmt).scalar_one_or_none()
            return self._to_usuario(row)

    def atualizar_senha_hash(self, usuario_id: int, senha: str):
        senha_hash = generate_password_hash(senha)
        with self._session() as session:
            usuario = session.get(UsuarioORM, usuario_id)
            usuario.senha_hash = senha_hash

    def salvar_codigo_recuperacao(self, usuario_id: int, codigo: str, validade_minutos: int = 15):
        agora = datetime.now(timezone.utc)
        expira_em = agora + timedelta(minutes=validade_minutos)
        codigo_hash = generate_password_hash(codigo)

        with self._session() as session:
            stmt = (
                select(RecuperacaoSenhaORM)
                .where(RecuperacaoSenhaORM.usuario_id == usuario_id)
                .where(RecuperacaoSenhaORM.usado_em == None)
            )
            for registro in session.execute(stmt).scalars().all():
                registro.usado_em = agora.isoformat(timespec="seconds")

            novo = RecuperacaoSenhaORM(
                usuario_id=usuario_id,
                codigo_hash=codigo_hash,
                expira_em=expira_em.isoformat(timespec="seconds"),
                criado_em=agora.isoformat(timespec="seconds"),
            )
            session.add(novo)
            session.flush()
            return novo.id

    def validar_codigo_recuperacao(self, usuario_id: int, codigo: str) -> bool:
        agora = datetime.now(timezone.utc)
        with self._session() as session:
            stmt = (
                select(RecuperacaoSenhaORM)
                .where(RecuperacaoSenhaORM.usuario_id == usuario_id)
                .where(RecuperacaoSenhaORM.usado_em == None)
                .order_by(RecuperacaoSenhaORM.id.desc())
            )
            for registro in session.execute(stmt).scalars().all():
                expira_em = datetime.fromisoformat(registro.expira_em)
                if expira_em < agora:
                    continue
                if check_password_hash(registro.codigo_hash, codigo):
                    return True
        return False

    def marcar_codigos_recuperacao_usados(self, usuario_id: int):
        agora = datetime.now(timezone.utc).isoformat(timespec="seconds")
        with self._session() as session:
            stmt = (
                select(RecuperacaoSenhaORM)
                .where(RecuperacaoSenhaORM.usuario_id == usuario_id)
                .where(RecuperacaoSenhaORM.usado_em == None)
            )
            for registro in session.execute(stmt).scalars().all():
                registro.usado_em = agora

    # --- Emails autorizados ---

    def autorizar_email(self, email: str, criado_em: str):
        with self._session() as session:
            novo = EmailAutorizadoORM(email=email.lower(), usado=0, criado_em=criado_em)
            session.add(novo)

    def email_esta_autorizado(self, email: str) -> bool:
        with self._session() as session:
            stmt = select(EmailAutorizadoORM).where(
                EmailAutorizadoORM.email == email.lower(),
                EmailAutorizadoORM.usado == 0,
            )
            return session.execute(stmt).scalar_one_or_none() is not None

    def marcar_email_usado(self, email: str):
        with self._session() as session:
            stmt = select(EmailAutorizadoORM).where(
                EmailAutorizadoORM.email == email.lower(),
                EmailAutorizadoORM.usado == 0,
            )
            row = session.execute(stmt).scalar_one_or_none()
            if row:
                row.usado = 1

    def buscar_emails_autorizados(self) -> list[dict]:
        with self._session() as session:
            rows = session.execute(select(EmailAutorizadoORM)).scalars().all()
            return [
                {"id": r.id, "email": r.email, "usado": r.usado, "criado_em": r.criado_em}
                for r in rows
            ]

    def revogar_email(self, email_id: int):
        with self._session() as session:
            row = session.get(EmailAutorizadoORM, email_id)
            if row:
                session.delete(row)

    def _senha_parece_hash(self, senha_salva: str) -> bool:
        return isinstance(senha_salva, str) and senha_salva.startswith(("pbkdf2:", "scrypt:"))

    def verificar_senha(self, usuario, senha: str) -> bool:
        if not usuario:
            return False
        senha_salva = usuario.senha_hash or ""

        if self._senha_parece_hash(senha_salva):
            return check_password_hash(senha_salva, senha)

        if senha_salva == senha:
            self.atualizar_senha_hash(usuario.id, senha)
            return True

        return False
