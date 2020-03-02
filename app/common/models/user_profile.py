from sqlalchemy import Column, Integer, String, ForeignKey
from app.common.database import db
from sqlalchemy.orm import relationship


class UserProfile(db.BaseModel):
    __tablename__ = 'user_profile'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(length=256))
    last_name = Column(String(length=256))
    phone = Column(String(length=15))
    user_id = Column(Integer, ForeignKey('user.id'))

    user = relationship("User")

    def __init__(self, first_name, last_name, phone, user_id):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.user_id = user_id

    def serialized(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone": self.phone
        }
