from typing import cast

from litestar import Litestar
from litestar.datastructures import State
from users_store.pg.core import AsyncSessionMaker, engine_factory, session_maker_factory
from users_store.pg.repositories import PasswordRepository, UserRepository

from users_api.web.settings import settings
from users_api.web.usecases import (
    PasswordUsecase,
    PasswordUsecaseProtocol,
    UserUsecase,
    UserUsecaseProtocol,
)


def create_pg_sessionmaker(app: Litestar):
    app.state.pg_engine = engine_factory(**settings.model_dump())
    app.state.pg_sessionmaker = session_maker_factory(app.state.pg_engine)
    return cast("AsyncSessionMaker", app.state.pg_sessionmaker)


async def provide_user_usecase(state: State) -> UserUsecaseProtocol:
    return UserUsecase(user_repository=UserRepository(state.pg_sessionmaker))


async def provide_password_usecase(state: State) -> PasswordUsecaseProtocol:
    return PasswordUsecase(
        password_repository=PasswordRepository(state.pg_sessionmaker)
    )
