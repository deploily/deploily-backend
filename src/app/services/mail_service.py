# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText

from flask import current_app, render_template

from app import db
from app.core.models import Mail

# TODO check if this file is relevant and remove if not


def render_email_template(template_name, **context):
    return render_template(f"emails/{template_name}", **context)


def send_and_log_email(to, subject, body, from_email=None):
    mail = Mail(
        title=subject,
        email_from=from_email or current_app.config["MAIL_USERNAME"],
        email_to=to,
        body=body,
        mail_state="outGoing",
    )
    db.session.add(mail)
    db.session.flush()

    try:
        msg = MIMEText(body, "html")
        msg["Subject"] = subject
        msg["From"] = mail.email_from
        msg["To"] = mail.email_to

        smtp_host = current_app.config["MAIL_HOST"]
        smtp_port = int(current_app.config["MAIL_PORT"])
        smtp_user = current_app.config["MAIL_USERNAME"]
        smtp_pass = current_app.config["MAIL_PASSWORD"]

        server = smtplib.SMTP_SSL(host=smtp_host, port=smtp_port)
        server.set_debuglevel(1)
        server.login(smtp_user, smtp_pass)
        server.sendmail(msg["From"], [msg["To"]], msg.as_string())
        server.quit()

        mail.mail_state = "sent"
        db.session.commit()
    except Exception as e:
        current_app.logger.error(f"Erreur envoi email à {to}: {e}")
        mail.mail_state = "error"

        db.session.commit()
    return mail
