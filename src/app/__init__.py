import logging
from flask import Flask
from flask_appbuilder import SQLA, AppBuilder
from flask_cors import CORS
from flask_migrate import Migrate
from sqlalchemy import MetaData

from app.custom_sso_security_manager import CustomSsoSecurityManager

app = Flask(__name__)
app.config.from_object("config")

# TODO move urls to .env | localhost should only be available for dev
CORS(
    app,
    resources={
        r"/api/*": {"origins": "[“http://localhost:3000”, “https://console.deploily.cloud“]"}
    },
    origins=["http://localhost:3000", "https://console.deploily.cloud"],
)


convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=convention)
db = SQLA(app, metadata=metadata)

migrate = Migrate(app, db, render_as_batch=True)

# appbuilder = AppBuilder(app, db.session)
appbuilder = AppBuilder(app, db.session, security_manager_class=CustomSsoSecurityManager)

"""Cron configuartion"""
if app.config["SCHEDULER_ENABLED"] in ["True", "true", "t", "1"]:
    from flask_apscheduler import APScheduler

    scheduler = APScheduler()
    scheduler.init_app(app)
    logging.getLogger("apscheduler").setLevel(logging.INFO)
    from . import schedulers

    scheduler.start()
# Register views

if __name__ == "__main__":
    app.run(debug=True)


from .core import models, views, controllers
from .service_api import models, views, controllers
from .service_apps import models, views, controllers
from . import services, schedulers
