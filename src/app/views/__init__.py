from app import appbuilder, db

from . import (
    cart_line_views,
    cart_views,
    parameters_value_views,
    service_parameters_views,
    service_views,
    support_ticket_views,
)

appbuilder.add_link(
    name="Swagger documentation",
    href="/swagger/v1",
    icon="fa-solid fa-book",
    # category_icon="fa-solid fa-cogs",
    category="Configuration",
)
