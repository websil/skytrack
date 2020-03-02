from sqlalchemy import Column, Integer, String, ForeignKey
from app.common.database import db
from sqlalchemy.orm import relationship


class UserAddress(db.BaseModel):
    __tablename__ = 'user_address'

    id = Column(Integer, primary_key=True)
    address = Column(String(length=512))
    user_id = Column(Integer, ForeignKey('user.id'))

    user = relationship("User")

    def __init__(self, address, user_id):
        self.address = address
        self.user_id = user_id

    def serialized(self):
        return {
            "address": self.address
        }
