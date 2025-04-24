from uuid import UUID

import pytest_asyncio
from users_core.models import Password, User


class MockUserRepository:
    def __init__(self, user: User):
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
    def __init__(self, password: Password):
        self.store = {
            password.user_id: password,
        }

    async def get_by_obj(self, obj: Password) -> Password:
        return self.store[obj.user_id]

    async def create(self, password: Password) -> None:
        self.store[password.user_id] = password

    async def delete(self, password: Password) -> None:
        self.store.pop(password.user_id)


@pytest_asyncio.fixture
async def mock_user():
    yield User(username="user1", email="user1@host")


@pytest_asyncio.fixture
async def mock_user_repository(mock_user):
    yield MockUserRepository(mock_user)


@pytest_asyncio.fixture
async def mock_password(mock_user):
    yield Password(user_id=mock_user.id, raw="Pass@12345")


@pytest_asyncio.fixture
async def mock_password_repository(mock_password):
    yield MockPasswordRepository(mock_password)
