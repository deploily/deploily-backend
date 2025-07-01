from sqlalchemy import Column, ForeignKey, Integer, Table

from app import db

association_table = Table(
    "app_service_version",
    db.Model.metadata,
    Column("app_service_id", Integer, ForeignKey("app_service.id")),
    Column("app_version_id", Integer, ForeignKey("version.id")),
)
