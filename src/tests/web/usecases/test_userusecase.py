import pytest

from users_api.web.scheme import CreateUserInputSchema, UpdateUserInputSchema
from users_api.web.usecases import UserUsecase


@pytest.mark.asyncio
async def test_get_by_id(mock_user_repository, mock_user):
    usecase = UserUsecase(user_repository=mock_user_repository)
    result = await usecase.get_by_id(user_id=mock_user.id)
    assert result.id == mock_user.id
    assert result.username == mock_user.username
    assert result.email == mock_user.email


@pytest.mark.asyncio
async def test_create_user(mock_user_repository):
    usecase = UserUsecase(user_repository=mock_user_repository)
    input_schema = CreateUserInputSchema(username="user1", email="user1@host")
    result = await usecase.create_user(data=input_schema)
    assert result is None


@pytest.mark.asyncio
async def test_update_user(mock_user_repository, mock_user):
    usecase = UserUsecase(user_repository=mock_user_repository)
    input_schema = UpdateUserInputSchema(email="user1@host1")
    result = await usecase.update_user(user_id=mock_user.id, data=input_schema)
    assert result is None


@pytest.mark.asyncio
async def test_delete_user(mock_user_repository, mock_user):
    usecase = UserUsecase(user_repository=mock_user_repository)
    result = await usecase.delete_user(user_id=mock_user.id)
    assert result is None
