import os
from user_data import client_data
from smtplib import SMTP
from string import Template
from pathlib import Path
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_welcome_email(destinatario, nome, client_code):

    load_dotenv()

    ROOT_PATH_EMAIL = Path(__file__).parent / 'confirm_email.html'

    remetente = os.getenv('EMAIL_BANK', '')

    smtp_server = os.getenv('SMTP_SERVER_GMAIL', '')
    smtp_port = os.getenv('SMTP_SERVER_PORT', '')
    smtp_username = os.getenv('EMAIL_BANK', '')
    smtp_password = os.getenv('EMAIL_BANK_PASSWORD', '')

    client_data = {"nome": nome, "email": destinatario, "code": client_code}

    with open(ROOT_PATH_EMAIL, 'r', encoding='utf-8') as email_html:
        text_email = email_html.read()
        template_sub = Template(text_email)
        email_content = template_sub.substitute(client_data)

    mime_email = MIMEMultipart()
    mime_email['from'] = remetente
    mime_email['to'] = destinatario
    mime_email['subject'] = 'Bem-vindo ao nosso banco! :)'

    mime_email.attach(MIMEText(email_content, 'html'))

    try:
        with SMTP(smtp_server, smtp_port) as server:
            server.ehlo()
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(mime_email)
        print("\n=== O Email de confirmação foi enviado com sucesso para seu email! ===\nCheque sua caixa de entrada e confirme abaixo.")
    except Exception as e:
        print(f"\n@@@ Erro ao enviar email: {e} @@@")