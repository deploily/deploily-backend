# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey, Integer, String, Text

from app.service_apps.models.app_service_subscription_model import (
    SubscriptionAppService,
)


class TtkEpaySubscriptionAppService(SubscriptionAppService):
    __tablename__ = "ttk_epay_subscription_app_service"
    id = Column(Integer, ForeignKey("subscription_app_service.id"), primary_key=True)
    __mapper_args__ = {
        "polymorphic_identity": "ttk_epay",
    }
    api_secret_key = Column(String, nullable=True)
    client_site_url = Column(String, nullable=True)
    client_site_name = Column(String, nullable=True)
    client_site_logo_url = Column(String, nullable=True)
    client_site_privacy = Column(String, nullable=True)
    client_site_terms = Column(String, nullable=True)
    client_site_phone_number = Column(String, nullable=True)
    client_site_address = Column(String, nullable=True)
    client_site_email = Column(String, nullable=True)
    satim_server_url = Column(String, nullable=True)
    satim_base_url = Column(String, nullable=True)
    satim_fail_url = Column(String, nullable=True)
    satim_confirm_url = Column(String, nullable=True)
    satim_client_server_url = Column(String, nullable=True)
    satim_user_name = Column(String, nullable=True)
    satim_password = Column(String, nullable=True)
    satim_terminal_id = Column(String, nullable=True)
    satim_language = Column(String, nullable=True)
    satim_description = Column(String, nullable=True)
    satim_currency = Column(String, nullable=True)
    satim_json_params = Column(Text, nullable=True)
    mvc_satim_server_url = Column(String, nullable=True)
    mvc_satim_fail_url = Column(String, nullable=True)
    mvc_satim_confirm_url = Column(String, nullable=True)
