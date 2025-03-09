# -*- coding: utf-8 -*-

from flask_appbuilder import ModelView
from app.models.user_models import MyUser
from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from app import appbuilder, db
from flask_appbuilder import ModelView, expose, has_access
from flask import redirect, url_for

from flask_appbuilder.security.sqla.models import User


class MyUserView(ModelView):
    datamodel = SQLAInterface(MyUser)
    list_columns = [
        "username",
        "email",
        "active",
        "roles",
        "phone"
    ]
    show_columns = ["username", "email", "active", "roles", "phone"]
    edit_columns = ["username", "email", "active", "roles", "phone"]
    add_columns = ["username", "email", "active", "roles", "phone"]


appbuilder.add_view(
    MyUserView, "List Users", icon="fa-user", category="Security"
)
