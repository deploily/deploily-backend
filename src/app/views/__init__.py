from app import appbuilder, db

from . import (
    parameters_value_views,
    payment_views,
    plan_views,
    profile_views,
    promo_code_views,
    service_parameters_views,
    service_plan_option_views,
    service_plan_views,
    service_tag_views,
    service_views,
    subscribe_views,
    support_ticket_response_views,
    support_ticket_views,
    user_views,
    contact_us,
    my_favorites_views,
)

appbuilder.add_link(
    name="Swagger documentation",
    href="/swagger/v1",
    icon="fa-solid fa-book",
    # category_icon="fa-solid fa-cogs",
    category="Configuration",
)
