from litestar import Litestar

from users_api.web.settings import settings

litestar = Litestar(
    route_handlers=[],
    debug=settings.DEBUG,
)
