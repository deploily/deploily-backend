# -*- coding: utf-8 -*-

from flask_appbuilder import Model
from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship


class RecommendationAppService(Model):
    id = Column(Integer, primary_key=True)
    # many-to-many relationship
    app_services = relationship(
        "AppService", secondary="app_service_recommendation", back_populates="recommended_apps"
    )

    def __repr__(self):
        return f"RecommendationAppService(id={self.id})"
