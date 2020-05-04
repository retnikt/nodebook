from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import jinja2
from aiosmtplib import SMTP  # type: ignore

from notebook.settings import settings

templates = jinja2.Environment(
    loader=jinja2.FileSystemLoader("templates/email"),
    autoescape=False,
    enable_async=True,
)


smtp = SMTP(
    hostname=settings.smtp_hostname,
    port=settings.smtp_port,
    username=settings.smtp_username,
    password=settings.smtp_password,
    use_tls=settings.smtp_direct_tls,
    start_tls=settings.smtp_start_tls,
)


async def connect():
    all(
        (
            settings.smtp_hostname,
            settings.smtp_port,
            settings.smtp_username,
            settings.smtp_password,
        )
    ) and await smtp.connect()


async def disconnect():
    # noinspection PyStatementEffect
    smtp.is_connected and await smtp.quit()


async def send_message(to, subject, template, /, **values):
    message = MIMEMultipart()
    message["From"] = settings.smtp_from
    message["To"] = to
    message["Subject"] = subject

    plain_template = templates.get_template(template + ".txt")
    plain = await plain_template.render_async(**values)
    plain_message = MIMEText(plain, "plain", "utf-8")
    message.attach(plain_message)

    await smtp.send_message(message)
