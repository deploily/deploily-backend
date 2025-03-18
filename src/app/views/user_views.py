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
        "credits",
        "roles",
        "phone",
        "profiles"
    ]
    show_columns = ["username", "email",
                    "active", "roles", "phone", "profiles"]
    edit_columns = ["username", "email",
                    "active", "roles", "phone", "profiles"]
    add_columns = ["username", "email", "active", "roles", "phone", "profiles"]


appbuilder.add_view(
    MyUserView, "List Users", icon="fa-user", category="Security"
)
