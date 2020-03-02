from app.api.controllers.user_controller import UserController
from app.api.controllers.cart_controller import CartController
from app.api.controllers.product_controller import ProductController


def setup_routes(app):
    user_controller = UserController()
    cart_controller = CartController()
    product_controller = ProductController()

    app.router.add_post('/v1/auth/login', user_controller.login, name="login")
    app.router.add_get('/v1/auth/logout', user_controller.logout, name="logout")
    app.router.add_get('/v1/user/profile', user_controller.profile, name="profile")

    app.router.add_put('/v1/store/cart', cart_controller.add, name="add_cart")
    app.router.add_get('/v1/store/cart', cart_controller.list, name="list_cart")

    app.router.add_get('/v1/store/product', product_controller.list, name="list_product")
