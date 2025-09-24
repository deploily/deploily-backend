from flask_appbuilder import Model
from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship


class CustomParameter(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    # parameter_type = Column(Enum("string", "int", name="string"))
    value = Column(String(255), nullable=False)
    deployment_subscription_id = Column(Integer, ForeignKey("subscription_deployment_service.id"))
    deployment_subscription = relationship("SubscriptionDeploymentService")

    def __repr__(self):
        return str(self.id)
