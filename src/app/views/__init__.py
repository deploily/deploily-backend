from . import test_views




from app import appbuilder, db

appbuilder.add_link(
    name="Swagger documentation",
    href="/swagger/v1",
    icon="fa-solid fa-book",
    # category_icon="fa-solid fa-cogs",
    category="Configuration",
)
