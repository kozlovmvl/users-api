import uuid

import pytest
from users_core.models import User
from users_store.pg.exc import DuplicateUserKey, UserNotFound

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
async def test_get_by_id_non_existet_user(mock_user_repository):
    usecase = UserUsecase(user_repository=mock_user_repository)
    with pytest.raises(UserNotFound):
        await usecase.get_by_id(user_id=uuid.uuid4())


@pytest.mark.asyncio
async def test_create_user(mock_user_repository):
    usecase = UserUsecase(user_repository=mock_user_repository)
    input_schema = CreateUserInputSchema(username="user2", email="user2@host")
    result = await usecase.create_user(data=input_schema)
    assert result is None


@pytest.mark.asyncio
async def test_create_existing_user(mock_user_repository, mock_user):
    usecase = UserUsecase(user_repository=mock_user_repository)
    input_schema = CreateUserInputSchema(
        username=mock_user.username, email=mock_user.email
    )
    with pytest.raises(DuplicateUserKey):
        await usecase.create_user(data=input_schema)


@pytest.mark.asyncio
async def test_update_user(mock_user_repository, mock_user):
    usecase = UserUsecase(user_repository=mock_user_repository)
    input_schema = UpdateUserInputSchema(email="user2@host1")
    result = await usecase.update_user(user_id=mock_user.id, data=input_schema)
    assert result is None


@pytest.mark.asyncio
async def test_update_user_with_duplicate_keys(mock_user_repository, mock_user):
    other_user = User(username="user2", email="user2@host")
    await mock_user_repository.create(other_user)

    usecase = UserUsecase(user_repository=mock_user_repository)
    input_schema = UpdateUserInputSchema(email=other_user.email)
    with pytest.raises(DuplicateUserKey):
        await usecase.update_user(user_id=mock_user.id, data=input_schema)


@pytest.mark.asyncio
async def test_delete_user(mock_user_repository, mock_user):
    usecase = UserUsecase(user_repository=mock_user_repository)
    result = await usecase.delete_user(user_id=mock_user.id)
    assert result is None
