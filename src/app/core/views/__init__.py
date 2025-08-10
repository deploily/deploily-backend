from app import appbuilder, db

from . import (
    service_tag_views,
    service_plan_option_views,
    service_plan_views,
    plan_views,
    service_views,
    subscription_views,
    support_ticket_views,
    payment_views,
    payment_profile_views,
    support_ticket_response_views,
    user_views,
    contact_us,
    my_favorites_views,
    mail_views,
    comment_views,
    rating_views,
    media_views,
    promo_code_views,
    managed_ressource_view,
)

appbuilder.add_link(
    name="Swagger documentation",
    href="/swagger/v1",
    icon="fa-solid fa-book",
    # category_icon="fa-solid fa-cogs",
    category="Configuration",
)
