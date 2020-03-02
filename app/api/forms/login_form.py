from app.common.forms.base import BaseForm
from app.common.auth import check_credentials


class LoginForm (BaseForm):

    login = ''
    password = ''

    """атрибуты которые можно массово загружать в класс"""
    safe_attributes = [
        'login',
        'password'
    ]

    messages = {
        'login.required': 'Login required',
        'login.user_not_found': 'Login or password is incorrect',
        'password.required': 'Password required',
    }

    async def validate(self):

        self.login = self.login.strip()
        self.password = self.password.strip()

        # валидация обязательного поля
        if not self.login:
            code = 'login.required'
            self.add_error(attribute='login', code=code, message=self.messages[code])

        # проверяем наличие пользователя
        if not await check_credentials(self.login, self.password):
            code = 'login.user_not_found'
            self.add_error(attribute='login', code=code, message=self.messages[code])

        # валидация обязательного поля
        if not self.password:
            code = 'password.required'
            self.add_error(attribute='password', code=code, message=self.messages[code])

        return not self.has_error()
