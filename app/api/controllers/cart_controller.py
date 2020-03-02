from aiohttp import web

from app.api.controllers.base import BaseController
from app.api.forms.cart_form import CartForm
from app.common.models.cart import Cart
from aiohttp_security import (authorized_userid, check_authorized)


class CartController(BaseController):

    """ метод добавления товара в корзину"""
    async def add(self, request: web.Request) -> web.Response:
        await check_authorized(request)

        form = CartForm()
        form.user_id = await authorized_userid(request)
        form.load(await request.post())
        if form.validate() and form.add():
            return self.response(body='OK')
        return self.response(body={'errors': form.errors})

    """метод отдает список товаров добавленных в корзину"""
    async def list(self, request: web.Request) -> web.Response:
        await check_authorized(request)

        products = [product.serialized() for product in Cart.find_by_user(user_id=await authorized_userid(request))]
        return self.response(body=products)
