from http import HTTPStatus

import pytest
from litestar import Litestar
from litestar.testing import AsyncTestClient
from users_core.models import Password, User


@pytest.mark.asyncio
async def test_create_password(api_client: AsyncTestClient[Litestar], mock_user: User):
    data = {"value": "Pass@12345"}
    response = await api_client.post(
        url=f"/password/{mock_user.id}",
        json=data,
    )
    assert response.status_code == HTTPStatus.CREATED


@pytest.mark.asyncio
async def test_update_password(
    api_client: AsyncTestClient[Litestar], mock_user: User, mock_password: Password
):
    data = {
        "current": mock_password.raw,
        "new": "Pass!12345",
    }
    response = await api_client.patch(
        url=f"/password/{mock_user.id}",
        json=data,
    )
    assert response.status_code == HTTPStatus.OK
