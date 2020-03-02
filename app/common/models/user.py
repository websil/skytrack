import enum

from sqlalchemy import Column, Integer, String, Enum
from datetime import time
from app.common.database import db
from sqlalchemy.orm import relationship


class UserStatus(enum.Enum):
    STATUS_ACTIVE = 'active'
    STATUS_BLOCKED = 'blocked'


class User(db.BaseModel):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    login = Column(String(length=50))
    email = Column(String(length=50))
    password = Column(String(length=50))
    status_const = Column(String(length=50))
    created_at = Column(Integer)
    last_visit_at = Column(Integer)

    profile = relationship("UserProfile", back_populates="user", uselist=False)
    addresses = relationship("UserAddress", back_populates="user")

    def __init__(self, login, password, status_const, email, created_at):
        self.login = login
        self.email = email
        self.password = password
        self.status_const = status_const
        self.created_at = created_at

    @staticmethod
    def find_by_id(user_id):
        return db.Session.query(User).filter_by(id=user_id, status_const=UserStatus.STATUS_ACTIVE.value).first()

    def serialized(self):
        return {
            "id": str(self.id) if self.id else None,
            "login": self.login,
            "email": self.email,
            "created_at": self.created_at if self.created_at else None,
        }
