import enum

from sqlalchemy import Column, Integer, Text, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.common.database import db


class ProductStatus(enum.Enum):
    STATUS_ACTIVE = 'active'
    STATUS_INACTIVE = 'inactive'
    STATUS_DELETED = 'deleted'


class Product(db.BaseModel):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    title = Column(String(length=1024))
    description = Column(Text)
    count = Column(Integer)
    shop_id = Column(Integer, ForeignKey('shop.id'))
    category_id = Column(Integer, ForeignKey('product_category.id'))
    status_const = Column(String(length=20))
    created_at = Column(Integer)

    shop = relationship("Shop")
    product_category = relationship("ProductCategory")

    def __init__(self, title, description, count, shop_id, category_id, status_const, created_at):
        self.title = title
        self.count = count
        self.description = description
        self.shop_id = shop_id
        self.category_id = category_id
        self.status_const = status_const
        self.created_at = created_at

    def serialized(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "created_at": self.created_at
        }

    @staticmethod
    def find_by_id(id):
        return db.Session\
            .query(Product)\
            .filter_by(id=id)\
            .first()