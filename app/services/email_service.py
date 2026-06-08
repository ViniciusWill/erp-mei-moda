import os
import smtplib
from email.message import EmailMessage


class EmailConfigError(RuntimeError):
    pass


def enviar_email_recuperacao(destinatario: str, codigo: str):
    host = os.environ.get("SMTP_HOST", "").strip()
    port = int(os.environ.get("SMTP_PORT", "587"))
    usuario = os.environ.get("SMTP_USER", "").strip()
    senha = os.environ.get("SMTP_PASSWORD", "").strip()
    remetente = os.environ.get("SMTP_FROM", usuario).strip()
    usar_tls = os.environ.get("SMTP_USE_TLS", "true").lower() != "false"

    if not host or not remetente:
        raise EmailConfigError("Configure SMTP_HOST e SMTP_FROM para enviar emails.")

    valores = " ".join([usuario, senha, remetente]).lower()
    if "seu-email" in valores or "sua-senha" in valores:
        raise EmailConfigError("Atualize o .env com o email real e a senha de app do provedor.")

    mensagem = EmailMessage()
    mensagem["Subject"] = "Codigo de recuperacao de senha"
    mensagem["From"] = remetente
    mensagem["To"] = destinatario
    mensagem.set_content(
        "\n".join(
            [
                "Voce solicitou a recuperacao de senha do ERP MEI Moda.",
                "",
                f"Seu codigo de recuperacao e: {codigo}",
                "",
                "Esse codigo expira em 15 minutos.",
                "Se voce nao solicitou essa alteracao, ignore este email.",
            ]
        )
    )

    with smtplib.SMTP(host, port, timeout=20) as servidor:
        if usar_tls:
            servidor.starttls()
        if usuario and senha:
            servidor.login(usuario, senha)
        servidor.send_message(mensagem)
