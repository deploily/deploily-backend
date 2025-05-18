# -*- coding: utf-8 -*-

from flask_appbuilder import Model
from flask_appbuilder.models.mixins import ImageColumn
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship


class ProvidersRessourceService(Model):
    id = Column(Integer, primary_key=True)

    name = Column(String(150))

    logo = Column(ImageColumn)
    short_description = Column(String(255))
    contact_number = Column(String(50))
    website = Column(String(255))
    facebook_page = Column(String(255))
    instagram_page = Column(String(255))
    linkedin_page = Column(String(255))
    extra_info = Column(Text)
    mail_support = Column(String(255))
    mail_sailes = Column(String(255))
    mail_partnership = Column(String(255))
    phone_support = Column(String(50))
    phone_sailes = Column(String(50))
    phone_partnership = Column(String(50))
    ressource_services = relationship("RessourceService", back_populates="provider")
    affiliations = relationship("Affiliation", back_populates="provider")

    def __repr__(self):
        return f"Ressource Provider Service: {self.name} "
