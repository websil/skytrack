from aiohttp import web

from app.api.controllers.base import BaseController
from app.api.search.product_search import ProductSearch


class ProductController(BaseController):

    """метод отдает список товаров"""
    async def list(self, request: web.Request) -> web.Response:
        form = ProductSearch()
        products = [product.serialized() for product in form.search(request.query)]
        return self.response(status=200, body=products)
