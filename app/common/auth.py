import hashlib

from aiohttp_security.abc import AbstractAuthorizationPolicy

from app.common.database import db
from app.common.models.user import User, UserStatus


class DBAuthorizationPolicy(AbstractAuthorizationPolicy):
    async def authorized_userid(self, identity):
        user = db.Session.query(User).filter_by(login=identity, status_const=UserStatus.STATUS_ACTIVE.value).first()
        if user:
            return user.id
        return None

    async def permits(self, identity, permission, context=None):
        if identity is None:
            return False
        return True


async def check_credentials(login, password):
    password = hashlib.md5(password.encode('utf-8')).hexdigest()
    return db.Session.query(
        db.Session.query(User).filter_by(login=login, password=password, status_const=UserStatus.STATUS_ACTIVE.value).exists()
    ).scalar()
