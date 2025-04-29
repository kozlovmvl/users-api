from collections.abc import AsyncIterator
from uuid import UUID

import pytest_asyncio
from litestar import Litestar
from litestar.testing import AsyncTestClient
from users_core.models import Password, User

from users_api.web.usecases import PasswordUsecase, UserUsecase


class MockUserRepository:
    def __init__(self, user: User, *args, **kwargs):
        self.store = {
            user.id: user,
        }

    async def get_by_id(self, user_id: UUID) -> User:
        return self.store[user_id]

    async def create(self, user: User) -> None:
        self.store[user.id] = user

    async def update(self, user: User) -> None:
        self.store[user.id] = user

    async def delete(self, user: User) -> None:
        self.store.pop(user.id)


class MockPasswordRepository:
    def __init__(self, password: Password, *args, **kwargs):
        self.store = {
            password.user_id: password,
        }

    async def get_by_obj(self, obj: Password) -> Password:
        return self.store[obj.user_id]

    async def create(self, password: Password) -> None:
        self.store[password.user_id] = password

    async def delete(self, password: Password) -> None:
        self.store.pop(password.user_id)


@pytest_asyncio.fixture()
async def mock_user():
    yield User(
        id=UUID("730a1a2c-92fd-424b-81e9-cfbcd8576ad4"),
        username="user1",
        email="user1@host",
    )


@pytest_asyncio.fixture()
async def mock_user_repository(mock_user):
    yield MockUserRepository(mock_user)


@pytest_asyncio.fixture()
async def mock_password(mock_user):
    yield Password(user_id=mock_user.id, raw="Pass@12345")


@pytest_asyncio.fixture()
async def mock_password_repository(mock_password):
    yield MockPasswordRepository(mock_password)


@pytest_asyncio.fixture(autouse=True)
async def patch_provide(mocker, mock_user_repository, mock_password_repository):
    async def mock_provide_user_usecase():
        return UserUsecase(user_repository=mock_user_repository)

    async def mock_provide_password_usecase():
        return PasswordUsecase(password_repository=mock_password_repository)

    mocker.patch("users_api.web.di.provide_user_usecase", new=mock_provide_user_usecase)
    mocker.patch(
        "users_api.web.di.provide_password_usecase", new=mock_provide_password_usecase
    )


@pytest_asyncio.fixture()
async def mock_app():
    from users_api.web.handlers import PasswordController, UserController

    yield Litestar(
        route_handlers=[UserController, PasswordController],
        debug=True,
    )


@pytest_asyncio.fixture()
async def api_client(mock_app) -> AsyncIterator[AsyncTestClient[Litestar]]:
    async with AsyncTestClient(app=mock_app) as client:
        yield client
