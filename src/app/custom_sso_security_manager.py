# -*- coding: utf-8 -*-

import logging

from flask import g
from flask_appbuilder.const import LOGMSG_WAR_SEC_LOGIN_FAILED
from flask_appbuilder.security.sqla.manager import SecurityManager

_logger = logging.getLogger(__name__)


class CustomSsoSecurityManager(SecurityManager):
    def oauth_user_info(self, provider, response=None):
        me = self.appbuilder.sm.oauth_remotes[provider].get("openid-connect/userinfo")
        me.raise_for_status()
        data = me.json()
        return {
            "username": data.get("preferred_username", ""),
            "first_name": data.get("given_name", ""),
            "last_name": data.get("family_name", ""),
            "email": data.get("email", ""),
            "role_keys": data.get("role_keys", []),
        }

    def load_user_jwt(self, _jwt_header, jwt_data):
        from app import appbuilder, db
        from app.models.payment_models import Payment
        from app.models.payment_profile_models import PaymentProfile

        username = jwt_data["preferred_username"]
        user = self.find_user(username=username)
        if user and user.is_active:
            # Set flask g.user to JWT user, we can't do it on before request
            existing_profile = (
                db.session.query(PaymentProfile)
                .filter_by(created_by=user, is_default_profile=True)
                .first()
            )
            if not existing_profile:
                payment_profile = PaymentProfile(
                    name=user.username,
                    profile_type="default",
                    created_by=user,
                    changed_by=user,
                    is_default_profile=True,
                )
                db.session.add(payment_profile)
                db.session.commit()

                payment = Payment(
                    amount=appbuilder.get_app.config["DEFAULT_CREDIT_AMOUNT"],
                    status="completed",
                    payment_method="cloud_credit",
                    profile_id=payment_profile.id,
                    created_by=user,
                    changed_by=user,
                )
                db.session.add(payment)
                db.session.commit()

                _logger.info(f"Payment profile created for existing user: {payment_profile}")
            g.user = user
            return user

        if user is None and self.auth_user_registration:

            user = self.add_user(
                username=username,
                first_name=jwt_data["family_name"],
                last_name=jwt_data["given_name"],
                email=jwt_data["email"],
                role=self.find_role(self.auth_user_registration_role),
            )
            g.user = user
            return user

        # If user does not exist on the DB and not auto user registration,
        # or user is inactive, go away.
        elif user is None or (not user.is_active):
            _logger.info(LOGMSG_WAR_SEC_LOGIN_FAILED, username)
            return None

        self.update_user_auth_stat(user)

        return None
