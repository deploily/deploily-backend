from flask_appbuilder import Model
from sqlalchemy import Column, Enum, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.models.service_plan_service_plan_option_association import (
    service_plan_option_association,
)


class ServicePlanOption(Model):
    id = Column(Integer, primary_key=True)

    icon = Column(String)
    html_content = Column(Text)
    option_type = Column(
        Enum("cpu", "ram", "disque", "request_limit", "other", name="option_type"), default="other"
    )
    option_value = Column(Integer)

    service_plans = relationship(
        "ServicePlan", secondary=service_plan_option_association, back_populates="options"
    )

    def __repr__(self):
        return f"{self.html_content}"

