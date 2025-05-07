import logging
import smtplib
from email.mime.text import MIMEText

from flask import current_app

from app import app, db, scheduler
from app.core.models import Mail

logger = logging.getLogger(__name__)


@scheduler.task("cron", id="send_pending_emails", max_instances=1, minute="*/1")
def send_pending_emails():
    with app.app_context():
        logger.info("[CRON] Sending pending emails - START")

        try:
            mails = db.session.query(Mail).filter_by(mail_state="outGoing").all()
            logger.info(f"[CRON] {len(mails)} emails to send found")
        except Exception as e:
            logger.error(f"[CRON] Error while fetching emails: {e}")
            return

        for mail in mails:
            try:
                msg = MIMEText(mail.body or "", "html")
                msg["Subject"] = mail.title or "(No subject)"
                msg["From"] = mail.email_from or current_app.config["MAIL_USERNAME"]
                msg["To"] = mail.email_to

                smtp_host = current_app.config["MAIL_HOST"]
                smtp_port = int(current_app.config["MAIL_PORT"])
                smtp_user = current_app.config["MAIL_USERNAME"]
                smtp_pass = current_app.config["MAIL_PASSWORD"]

                logger.debug(f"[CRON] Connecting to {smtp_host}:{smtp_port} with user {smtp_user}")

                server = smtplib.SMTP_SSL(host=smtp_host, port=smtp_port)
                server.set_debuglevel(1)
                server.login(smtp_user, smtp_pass)
                server.sendmail(msg["From"], [msg["To"]], msg.as_string())
                server.quit()

                mail.mail_state = "sent"
                db.session.commit()
                logger.info(f"[CRON] ✅ Email sent to {mail.email_to}")

            except Exception as e:
                logger.error(f"[CRON] ❌ Error sending to {mail.email_to}: {e}")
                mail.mail_state = "error"
                db.session.commit()

        logger.info("[CRON] Sending pending emails - END")
