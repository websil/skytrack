from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.common.database import db


class Cart(db.BaseModel):
    __tablename__ = 'cart'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    product_id = Column(Integer, ForeignKey('product.id'))
    amount = Column(Integer)
    created_at = Column(Integer)

    user = relationship("User")
    product = relationship("Product")

    def __init__(self, product_id, amount, created_at, user_id):
        self.user_id = user_id
        self.product_id = product_id
        self.amount = amount
        self.created_at = created_at

    def serialized(self):
        return {
            "product": self.product.serialized(),
            "amount": self.amount,
            "created_at": self.created_at
        }

    @staticmethod
    def find_by_user(user_id):
        return db.Session.query(Cart).filter_by(user_id=user_id).all()

