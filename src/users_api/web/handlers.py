from uuid import UUID

from litestar import Controller, delete, get, patch, post
from litestar.di import Provide
from users_store.pg.repositories import PasswordRepository, UserRepository

from users_api.web.scheme import (
    CreatePasswordInputSchema,
    CreateUserInputSchema,
    GetUserOutputSchema,
    UpdatePasswordInputSchema,
    UpdateUserInputSchema,
)
from users_api.web.usecases import (
    PasswordUsecase,
    PasswordUsecaseProtocol,
    UserUsecase,
    UserUsecaseProtocol,
)


def provide_user_usecase() -> UserUsecaseProtocol:
    return UserUsecase(user_repository=UserRepository())


def provide_password_usecase() -> PasswordUsecaseProtocol:
    return PasswordUsecase(password_repository=PasswordRepository())


class UserController(Controller):
    path = "/user"
    dependencies = {
        "usecase": Provide(provide_user_usecase),
    }

    @get("/{user_id:uuid}")
    async def get_user(
        self, user_id: UUID, usecase: UserUsecaseProtocol
    ) -> GetUserOutputSchema: ...

    @post("/")
    async def create_user(
        self, data: CreateUserInputSchema, usecase: UserUsecaseProtocol
    ) -> None: ...

    @patch("/{user_id:uuid}")
    async def update_user(
        self, user_id: UUID, data: UpdateUserInputSchema, usecase: UserUsecaseProtocol
    ) -> None: ...

    @delete("/{user_id:uuid}")
    async def delete_user(
        self, user_id: UUID, usecase: UserUsecaseProtocol
    ) -> None: ...


class PasswordController(Controller):
    path = "/password"
    dependencies = {
        "usecase": Provide(provide_password_usecase),
    }

    @post("/{user_id:uuid}")
    async def create_password(
        self, data: CreatePasswordInputSchema, usecase: PasswordUsecaseProtocol
    ) -> None: ...

    @patch("/{user_id:uuid}")
    async def update_password(
        self, data: UpdatePasswordInputSchema, usecase: PasswordUsecaseProtocol
    ) -> None: ...
