from http import HTTPStatus

import pytest
from litestar import Litestar
from litestar.testing import AsyncTestClient
from users_core.models import User


@pytest.mark.asyncio
async def test_get_user(api_client: AsyncTestClient[Litestar], mock_user: User):
    response = await api_client.get(url=f"/user/{mock_user.id}")
    assert response.status_code == HTTPStatus.OK


@pytest.mark.asyncio
async def test_create_user(api_client: AsyncTestClient[Litestar]):
    data = {"username": "user2", "email": "user2@host"}
    response = await api_client.post(
        url="/user",
        json=data,
    )
    assert response.status_code == HTTPStatus.CREATED


@pytest.mark.asyncio
async def test_update_user(api_client: AsyncTestClient[Litestar], mock_user: User):
    data = {"email": "user2@other-host"}
    response = await api_client.patch(
        url=f"/user/{mock_user.id}",
        json=data,
    )
    assert response.status_code == HTTPStatus.OK


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_user(api_client: AsyncTestClient[Litestar], mock_user: User):
    response = await api_client.delete(
        url=f"/user/{mock_user.id}",
    )
    assert response.status_code == HTTPStatus.NO_CONTENT
