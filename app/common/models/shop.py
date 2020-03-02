import enum

from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import time
from app.common.database import db


class ShopStatus(enum.Enum):
    STATUS_ACTIVE = 'active'
    STATUS_INACTIVE = 'inactive'
    STATUS_DELETED = 'deleted'


class Shop(db.BaseModel):
    __tablename__ = 'shop'

    id = Column(Integer, primary_key=True)
    title = Column(String(length=512))
    description = Column(Text)
    user_id = Column(Integer, ForeignKey('user.id'))
    status_const = Column(Enum(ShopStatus))
    created_at = Column(Integer)

    user = relationship("User")

    def __init__(self, title, description, user_id, status_const):
        self.title = title
        self.description = description
        self.user_id = user_id
        self.status_const = status_const
        self.created_at = time()
