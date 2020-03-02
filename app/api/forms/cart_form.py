import time

from app.common.models.product import Product, ProductStatus
from app.common.models.cart import Cart
from app.common.forms.base import BaseForm
from app.common.database import db


class CartForm (BaseForm):

    """ Форма валидации и добавления данных
    в корзину пользователя. """

    user_id = None
    product_id = None
    amount = 1

    """атрибуты которые можно массово загружать в класс"""
    safe_attributes = [
        'product_id',
        'amount'
    ]

    """ Сообщения для вывода ошибок """
    messages = {
        'product_id.required': 'Product id required',
        'product_id.product_not_found': 'Product not found',
        'product_id.exist_cart': 'Product is already in the cart',
        'amount.required': 'Amount required',
        'amount.not_found': 'Only {} item can be ordered',
    }

    def validate(self):
        self.amount = int(self.amount)

        # ИД товара должно быть обязательным параметром
        if not self.product_id:
            code = 'product_id.required'
            self.add_error(attribute='product_id', code=code, message=self.messages[code])

        # товар должен быть в наличии в базе, а также быть активированным
        product = Product.find_by_id(id=self.product_id)
        if not product or not product.status_const == ProductStatus.STATUS_ACTIVE.value:
            code = 'product_id.product_not_found'
            self.add_error(attribute='product_id', code=code, message=self.messages[code])

        # невозможно добавить в корзину два одинаковых товара
        exists = db.Session.query(
            db.Session.query(Cart).filter_by(product_id=self.product_id, user_id=self.user_id).exists()
        ).scalar()
        if exists:
            code = 'product_id.exist_cart'
            self.add_error(attribute='product_id', code=code, message=self.messages[code])

        # количестов товаров должно быть указано, по умолчанию количество товаров равно 1
        if not self.amount:
            code = 'amount.required'
            self.add_error(attribute='amount', code=code, message=self.messages[code])

        # товара должно быть достаточно для добавления
        if product and self.amount >= product.count:
            code = 'amount.not_found'
            self.add_error(attribute='amount', code=code, message=self.messages[code].format(product.count))

        return not self.has_error()

    def add(self):
        cart = Cart(amount=self.amount, product_id=self.product_id, created_at=time.time(), user_id=self.user_id)
        db.Session.add(cart)
        db.Session.commit()
        return True
