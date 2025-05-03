import uuid
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
async def test_get_non_existet_user(api_client: AsyncTestClient[Litestar]):
    response = await api_client.get(url=f"/user/{uuid.uuid4()}")
    assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.asyncio
async def test_create_user(api_client: AsyncTestClient[Litestar]):
    data = {"username": "user2", "email": "user2@host"}
    response = await api_client.post(
        url="/user",
        json=data,
    )
    assert response.status_code == HTTPStatus.CREATED


@pytest.mark.asyncio
async def test_create_existing_user(api_client: AsyncTestClient[Litestar], mock_user):
    data = {"username": mock_user.username, "email": mock_user.email}
    response = await api_client.post(
        url="/user",
        json=data,
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.parametrize(
    argnames=("username", "email"),
    argvalues=(
        ("us", "user@host"),
        ("username", "userhost"),
    ),
)
@pytest.mark.asyncio
async def test_create_user_with_invalid_data(
    api_client: AsyncTestClient[Litestar], username, email
):
    data = {"username": username, "email": email}
    response = await api_client.post(
        url="/user",
        json=data,
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.asyncio
async def test_update_user(api_client: AsyncTestClient[Litestar], mock_user: User):
    data = {"email": "user2@other-host"}
    response = await api_client.patch(
        url=f"/user/{mock_user.id}",
        json=data,
    )
    assert response.status_code == HTTPStatus.OK


@pytest.mark.asyncio
async def test_update_user_with_duplicate_keys(
    api_client: AsyncTestClient[Litestar], mock_user: User, mock_user_repository
):
    other_user = User(username="user2", email="user2@host")
    await mock_user_repository.create(other_user)

    data = {"email": other_user.email}
    response = await api_client.patch(
        url=f"/user/{mock_user.id}",
        json=data,
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.parametrize(
    argnames=("email",),
    argvalues=(("userhost",),),
)
@pytest.mark.asyncio
async def test_update_user_with_invalid_data(
    api_client: AsyncTestClient[Litestar], mock_user, email
):
    data = {"email": email}
    response = await api_client.patch(
        url=f"/user/{mock_user.id}",
        json=data,
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_user(api_client: AsyncTestClient[Litestar], mock_user: User):
    response = await api_client.delete(
        url=f"/user/{mock_user.id}",
    )
    assert response.status_code == HTTPStatus.NO_CONTENT
