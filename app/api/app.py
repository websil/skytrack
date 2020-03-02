#! /usr/bin/env python
import logging
import asyncio
import aioredis
from app.api.routes import setup_routes
from aiohttp import web

from aiohttp_session import setup as setup_session
from aiohttp_session.redis_storage import RedisStorage
from aiohttp_security import setup as setup_security
from aiohttp_security import SessionIdentityPolicy

from app.common.auth import DBAuthorizationPolicy

from app.common.database import db
from envparse import env

env.read_envfile('.env')


async def make_redis_pool():
    redis_address = (env.str('REDIS_HOSTNAME'), env.str('REDIS_PORT'))
    return await aioredis.create_redis_pool(redis_address, timeout=1)


async def dispose_redis_pool():
    redis_pool.close()
    await redis_pool.wait_closed()


"""настройка логирования"""
log = logging.getLogger(__name__)
logging.basicConfig(filename="log/debug.log", level=logging.DEBUG)

"""инициализация базы данных"""
db.initialize()

"""подлючение redis для хранения сессии"""
loop = asyncio.get_event_loop()
redis_pool = loop.run_until_complete(make_redis_pool())
storage = RedisStorage(redis_pool)

"""запуск сервера"""
app = web.Application()
setup_session(app, RedisStorage(redis_pool))
setup_security(app, SessionIdentityPolicy(), DBAuthorizationPolicy())

app.on_cleanup.append(dispose_redis_pool)
setup_routes(app)
