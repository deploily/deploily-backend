from flask import Flask
from flask_appbuilder import AppBuilder, SQLA
from sqlalchemy import MetaData
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object('config')

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

appbuilder = AppBuilder(app, db.session)


# Register views

if __name__ == "__main__":
    app.run(debug=True)

# from . import models
from . import views
from . import controllers
from . import services

