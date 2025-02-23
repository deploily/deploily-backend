# -*- coding: utf-8 -*-
import logging
import os

import pytest
from flask_appbuilder import SQLA
from flask_appbuilder import AppBuilder
from flask_appbuilder.security.sqla.models import Role
from sqlalchemy import MetaData

LOGGER = logging.getLogger(__name__)


@pytest.fixture()
def app():

    from flask import Flask

    flask_app = Flask(__name__)
    basedir = os.path.abspath(os.path.dirname(__file__))
    flask_app.config["AUTH_ROLE_ADMIN"] = "Admin"
    flask_app.config["TESTING"] = True
    flask_app.config["DEBUG"] = True
    flask_app.config["WTF_CSRF_ENABLED"] = False
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    # flask_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    #     basedir, "test_deploily.db"
    # )
    flask_app.config["JWT_COOKIE_CSRF_PROTECT"] = False
    flask_app.config["JWT_TOKEN_LOCATION"] = "headers"
    flask_app.config["JWT_HEADER_TYPE"] = "Bearer"
    flask_app.config["JWT_BLACKLIST_ENABLED"] = False
    flask_app.config["JWT_SECRET_KEY"] = "abcdefghijklmnopqrtu"
    flask_app.config["SECRET_KEY"] = "insecure_key_for_de"
    # Setup default language
    flask_app.config["BABEL_DEFAULT_LOCALE"] = "en"
    # Your application default translation path
    flask_app.config["BABEL_DEFAULT_FOLDER"] = "translations"
    # The allowed translation for you app
    flask_app.config["LANGUAGES"] = {
        "en": {"flag": "gb", "name": "English"},
        "fr": {"flag": "fr", "name": "French"},
    }
    from flask_babel import Babel

    Babel(flask_app)
    yield flask_app


@pytest.fixture
def db(app):
    convention = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
    metadata = MetaData(naming_convention=convention)
    """Fixture to provide the database."""
    yield SQLA(app, metadata=metadata)
    # yield flask_db


@pytest.fixture
def appbuilder(app, db):
    """Fixture to provide FlaskAppBuilder instance."""
    return AppBuilder(app, db.session)
    # yield flask_appbuilder


@pytest.fixture
def client(app, db):
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

        # Close the database session and drop all tables after the session
        # db.session.remove()
        # db.drop_all()


@pytest.fixture
def test_user(appbuilder, db):
    username = "test"
    password = "test"
    first_name = "testFirst"
    last_name = "testLast"
    email = "testuser@gmail.com"
    role_name = appbuilder.sm.auth_role_admin

    # Ensure the Admin role exists
    admin_role = db.session.query(Role).filter_by(name=role_name).first()
    if not admin_role:
        admin_role = Role(name=role_name)
        db.session.add(admin_role)
        db.session.commit()

    user = appbuilder.sm.find_user(username=username)
    if user:
        db.session.delete(user)
        db.session.commit()

    roles = [appbuilder.sm.find_role(role_name)]
    yield appbuilder.sm.add_user(
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
        role=roles,
        password=password,
    )
