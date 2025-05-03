import uuid

import pytest
from users_store.pg.exc import PasswordNotFound, UserNotFound

from users_api.web.scheme import CreatePasswordInputSchema, UpdatePasswordInputSchema
from users_api.web.usecases import PasswordUsecase


@pytest.mark.asyncio
async def test_create_password(mock_password_repository, mock_user):
    usecase = PasswordUsecase(password_repository=mock_password_repository)
    input_schema = CreatePasswordInputSchema(value="Pass@12345")
    result = await usecase.create_password(user_id=mock_user.id, data=input_schema)
    assert result is None


@pytest.mark.asyncio
async def test_create_password_non_existet_user(mock_password_repository):
    usecase = PasswordUsecase(password_repository=mock_password_repository)
    input_schema = CreatePasswordInputSchema(value="Pass@12345")
    with pytest.raises(UserNotFound):
        await usecase.create_password(user_id=uuid.uuid4(), data=input_schema)


@pytest.mark.asyncio
async def test_update_password(mock_password_repository, mock_password):
    usecase = PasswordUsecase(password_repository=mock_password_repository)
    await mock_password_repository.create(mock_password)
    input_schema = UpdatePasswordInputSchema(
        current=mock_password.raw, new="Pass!12345"
    )
    result = await usecase.update_password(
        user_id=mock_password.user_id, data=input_schema
    )
    assert result is None


@pytest.mark.asyncio
async def test_update_password_with_invalid_current(mock_password_repository):
    usecase = PasswordUsecase(password_repository=mock_password_repository)
    input_schema = UpdatePasswordInputSchema(current="Pass@12345", new="Pass!12345")
    with pytest.raises(PasswordNotFound):
        await usecase.update_password(user_id=uuid.uuid4(), data=input_schema)
