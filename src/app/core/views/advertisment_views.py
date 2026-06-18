from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder, db
from app.core.models.advertisment import Advertisement


class AdvertisementModelView(ModelView):
    route_base = "/admin/advertisement"
    datamodel = SQLAInterface(Advertisement)

    list_columns = [
        "name",
        "featured",
        "image_1920",
        "image_128",
        "description",
        "color",
        "advertisement_type",
    ]
    base_order = ("id", "desc")


db.create_all()
appbuilder.add_view(
    AdvertisementModelView,
    "Advertisement",
    icon="fa-solid fa-check-circle-o",
    category="Operations",
)
