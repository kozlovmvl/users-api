from litestar import Litestar

from users_api.web.di import create_pg_sessionmaker
from users_api.web.handlers import PasswordController, UserController

app = Litestar(
    route_handlers=[
        UserController,
        PasswordController,
    ],
    # debug=settings.debug,
    debug=True,
    on_startup=[create_pg_sessionmaker],
)
