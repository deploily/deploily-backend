from flask_appbuilder.security.sqla.manager import SecurityManager
from flask import g

class CustomSsoSecurityManager(SecurityManager):
    def oauth_user_info(self, provider, response=None):  # noqa: ARG002
        me = self.appbuilder.sm.oauth_remotes[provider].get(
            "openid-connect/userinfo"
        )
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
        username = jwt_data["preferred_username"]
        user = self.find_user(username=username)
        if user.is_active:
            # Set flask g.user to JWT user, we can't do it on before request
            g.user = user
            return user
        return None