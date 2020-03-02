from app.common.models.product import Product, ProductStatus
from app.common.forms.base import BaseForm
from app.common.database import db


class ProductSearch (BaseForm):

    # ИД магазина
    shop_id = None

    safe_attributes = [
        'shop_id'
    ]

    def validate(self):
        if self.shop_id:
            self.shop_id = int(self.shop_id)
        return True

    def search(self, params):
        self.load(params)
        if not self.validate():
            return []

        query = db.Session.query(Product).filter_by(status_const=ProductStatus.STATUS_ACTIVE.value)

        """поиск по shop_id"""
        if self.shop_id:
            query = query.filter_by(shop_id=self.shop_id)

        return query.all()
