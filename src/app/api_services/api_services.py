from sqlalchemy import Column, String
from app.models import Service


class ExtendedService(Service):
    __tablename__ = None
    __mapper_args__ = {
        'polymorphic_identity': 'extended_service'
    }

    _additional = Column("additional", String(255), nullable=True)

    @property
    def additional_field(self):
        """Affiche additional_field uniquement pour ExtendedService"""
        return self._additional if self.type == "extended_service" else None

    def __repr__(self):
        return f"ExtendedService: {self.name} - {self.additional_field or 'N/A'}"
