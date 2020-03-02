from sqlalchemy import Column, Integer, String
from app.common.database import db


class ProductCategory(db.BaseModel):
    __tablename__ = 'product_category'

    id = Column(Integer, primary_key=True)
    title = Column(String(length=1024))

    def __init__(self, title):
        self.title = title
