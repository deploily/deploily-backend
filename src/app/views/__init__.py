
from app import appbuilder, db
from . import cart_views
from . import cart_line_views
from . import service_views
from . import service_parameters_views
from . import parameters_value_views

appbuilder.add_link(
    name="Swagger documentation",
    href="/swagger/v1",
    icon="fa-solid fa-book",
    # category_icon="fa-solid fa-cogs",
    category="Configuration",
)
