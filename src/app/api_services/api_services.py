from sqlalchemy import Column, String

from app.models import Service


class ExtendedService(Service):
    __tablename__ = None
    __mapper_args__ = {"polymorphic_identity": "extended_service"}

    additional = Column("additional", String(255), nullable=True)

    def __repr__(self):
        return f"ExtendedService: {self.name} - {self.additional or 'N/A'}"
