# -*- coding: utf-8 -*-
import logging
import smtplib
from email.mime.text import MIMEText

from flask import app, current_app

from app import app, celery, db
from app.core.models.mail_models import Mail

# from app import app


_logger = logging.getLogger(__name__)


@celery.task
def send_mail(mail_id):
    with app.app_context():
        try:
            mail = db.session.query(Mail).filter(Mail.id == mail_id).first()
            if not mail:
                _logger.warning(f"[SEND MAIL TASK] THE EMAIL DON'T EXIST")
                return
            _logger.info("[CRON] Sending pending emails - START")
            msg = MIMEText(mail.body or "", "html")
            msg["Subject"] = mail.title or "(No subject)"
            msg["From"] = mail.email_from or current_app.config["MAIL_USERNAME"]
            msg["To"] = mail.email_to

            smtp_host = current_app.config["MAIL_HOST"]
            smtp_port = int(current_app.config["MAIL_PORT"])
            smtp_user = current_app.config["MAIL_USERNAME"]
            smtp_pass = current_app.config["MAIL_PASSWORD"]

            _logger.debug(f"[CRON] Connecting to {smtp_host}:{smtp_port} with user {smtp_user}")

            server = smtplib.SMTP_SSL(host=smtp_host, port=smtp_port)
            server.set_debuglevel(1)
            server.login(smtp_user, smtp_pass)
            server.sendmail(msg["From"], [msg["To"]], msg.as_string())
            server.quit()

            mail.mail_state = "sent"
            db.session.commit()
            _logger.info(f"[CRON] ✅ Email sent to {mail.email_to}")

        except Exception as e:
            _logger.error(f"[CRON] ❌ Error sending to {mail.email_to}: {e}")
            mail.mail_state = "error"
            db.session.commit()
