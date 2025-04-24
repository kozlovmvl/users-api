from typing import Protocol, runtime_checkable
from uuid import UUID

from users_core.models import Password, User
from users_store.pg.repositories import (
    PasswordRepositoryProtocol,
    UserRepositoryProtocol,
)

from users_api.web.scheme import (
    CreatePasswordInputSchema,
    CreateUserInputSchema,
    GetUserOutputSchema,
    UpdatePasswordInputSchema,
    UpdateUserInputSchema,
)


@runtime_checkable
class UserUsecaseProtocol(Protocol):
    async def get_by_id(self, user_id: UUID) -> GetUserOutputSchema: ...

    async def create_user(self, data: CreateUserInputSchema) -> None: ...

    async def update_user(self, user_id: UUID, data: UpdateUserInputSchema) -> None: ...

    async def delete_user(self, user_id: UUID) -> None: ...


@runtime_checkable
class PasswordUsecaseProtocol(Protocol):
    async def create_password(
        self, user_id: UUID, data: CreatePasswordInputSchema
    ) -> None: ...

    async def update_password(
        self, user_id: UUID, data: UpdatePasswordInputSchema
    ) -> None: ...


class UserUsecase:
    def __init__(self, user_repository: UserRepositoryProtocol):
        self.user_repository = user_repository

    async def get_by_id(self, user_id: UUID) -> GetUserOutputSchema:
        user = await self.user_repository.get_by_id(user_id)
        return GetUserOutputSchema.model_validate(user)

    async def create_user(self, data: CreateUserInputSchema) -> None:
        user = User.model_validate(data)
        await self.user_repository.create(user)

    async def update_user(self, user_id: UUID, data: UpdateUserInputSchema) -> None:
        user = await self.user_repository.get_by_id(user_id)
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(user, key, value)
        await self.user_repository.update(user)

    async def delete_user(self, user_id: UUID) -> None:
        user = await self.user_repository.get_by_id(user_id)
        await self.user_repository.delete(user)


class PasswordUsecase:
    def __init__(self, password_repository: PasswordRepositoryProtocol):
        self.password_repository = password_repository

    async def create_password(
        self, user_id: UUID, data: CreatePasswordInputSchema
    ) -> None:
        password = Password(user_id=user_id, raw=data.value)
        await self.password_repository.create(password)

    async def update_password(
        self, user_id: UUID, data: UpdatePasswordInputSchema
    ) -> None:
        current_password = Password(user_id=user_id, raw=data.current)
        result = await self.password_repository.get_by_obj(current_password)
        if result:
            await self.password_repository.delete(result)
            new_password = Password(user_id=user_id, raw=data.new)
            await self.password_repository.create(new_password)
