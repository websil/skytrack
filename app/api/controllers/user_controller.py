from aiohttp import web
from app.api.controllers.base import BaseController
from app.api.forms.login_form import LoginForm
from app.common.models.user import User
from aiohttp_security import (
    remember, forget, authorized_userid, check_authorized
)


class UserController(BaseController):

    """ Контроллер для обработки методов API
    которые связаны с работой над пользовательскими данным.
    Контроллер содержит 3 метода:

        profile - получение данных авторизированного профиля
        login - авторизация пользователя
        logout - разлогирование
    """

    async def profile(self, request: web.Request) -> web.Response:
        await check_authorized(request)
        user = User.find_by_id(await authorized_userid(request))
        if user:
            body = {
                **{'email': user.email},
                **user.profile.serialized(),
                **{'addresses': [user_address.serialized() for user_address in user.addresses]}
            }
            return self.response(status=200, body=body)
        return web.HTTPNotFound()

    async def login(self, request: web.Request) -> web.Response:
        user_id = await authorized_userid(request)
        if user_id:
            return self.response(body='OK')

        form = LoginForm()
        form.load(await request.post())

        if await form.validate():
            await remember(request, web.Response(), form.login)
            return self.response(body='OK')
        return self.response(status=422, body={'errors': form.errors})

    async def logout(self, request: web.Request):
        await check_authorized(request)
        await forget(request, web.Response())
        return self.response(body='OK')
