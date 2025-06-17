from sqlalchemy import Column, ForeignKey, Integer, Table

from app import db

association_table = Table(
    "app_service_recommendation",
    db.Model.metadata,
    Column("app_service_id", Integer, ForeignKey("app_service.id")),
    Column("recommendation_app_service_id", Integer, ForeignKey("recommendation_app_service.id")),
)
