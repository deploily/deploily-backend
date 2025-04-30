from app import appbuilder

if appbuilder.get_app.config["SCHEDULER_ENABLED"] in [
    "True",
    "true",
    "t",
    "1",
]:
    from . import send_pending_emails
