# -*- coding: utf-8 -*-
from flask_appbuilder import Model
from sqlalchemy import Column, Integer, DateTime, Enum, Boolean, ForeignKey
from sqlalchemy import DateTime
from datetime import datetime, timedelta
from sqlalchemy.orm import relationship


class PromoUsage(Model):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("ab_user.id"))
    user = relationship("MyUser")
    promo_code_id = Column(Integer, ForeignKey("promo_code.id"))
    promo_code = relationship("PromoCode") 
    used_at = Column(DateTime, default=lambda: datetime.now().replace(microsecond=0)
                     + timedelta(hours=48),
                     nullable=False,)

    def __repr__(self):
        return str(self.id)
