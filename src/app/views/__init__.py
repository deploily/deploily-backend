from app import appbuilder, db

from . import (
    cart_line_views,
    cart_views,
    parameters_value_views,
    service_parameters_views,
    service_views,
    support_ticket_views,
    support_ticket_response_views,
    user_views,
    my_favorites_views,
    contact_us,
    service_tag_views,
    my_service_views,
    service_plan_views,
    plan_views
)

appbuilder.add_link(
    name="Swagger documentation",
    href="/swagger/v1",
    icon="fa-solid fa-book",
    # category_icon="fa-solid fa-cogs",
    category="Configuration",
)
