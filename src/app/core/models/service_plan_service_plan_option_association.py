from flask_appbuilder import Model
from sqlalchemy import Column, ForeignKey, Integer, Table

service_plan_option_association = Table(
    "service_plan_option_association",
    Model.metadata,
    Column("service_plan_id", Integer, ForeignKey("service_plan.id"), primary_key=True),
    Column(
        "service_plan_option_id", Integer, ForeignKey("service_plan_option.id"), primary_key=True
    ),
)
