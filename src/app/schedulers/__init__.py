from app import appbuilder

if appbuilder.get_app.config["SCHEDULER_ENABLED"] in [
    "True",
    "true",
    "t",
    "1",
]:

    from . import delete_consumer
    from . import notify_subscription_expiration
    from . import notify_managed_ressource_expiraton
    from . import support_ticket_tasks
