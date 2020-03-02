import ujson as json

from typing import Any, List, Dict
from aiohttp import web


class BaseController:
    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def redirect(router, route_name):
        location = router[route_name].url_for()
        return web.HTTPFound(location)

    @classmethod
    def response(cls, body: Any = None, status: int = 200, reason: str = None,
                 headers: Dict[str, Any] = None) -> web.Response:
        json_body = json.dumps(body)

        return web.Response(
            text=json_body,
            status=status,
            reason=reason,
            headers=headers,
            charset="utf-8",
            content_type="application/json")