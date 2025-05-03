from uuid import UUID

from litestar import Controller, delete, get, patch, post
from litestar.di import Provide
from users_core.validators import (
    EmailInvalidStruct,
    PasswordInvalidLength,
    PasswordInvalidSymbol,
    UsernameIinvalidLength,
    UsernameInvalidSymbol,
)
from users_store.pg.exc import DuplicateUserKey, UserNotFound

from users_api.web.di import provide_password_usecase, provide_user_usecase
from users_api.web.exc import (
    handle_duplicate_user_key,
    handle_invalid_email_struct,
    handle_invalid_password_length,
    handle_invalid_password_symbol,
    handle_invalid_username_length,
    handle_invalid_username_symbol,
    handle_user_not_found,
)
from users_api.web.scheme import (
    CreatePasswordInputSchema,
    CreateUserInputSchema,
    GetUserOutputSchema,
    UpdatePasswordInputSchema,
    UpdateUserInputSchema,
)
from users_api.web.usecases import (
    PasswordUsecaseProtocol,
    UserUsecaseProtocol,
)


class UserController(Controller):
    path = "/user"
    dependencies = {
        "usecase": Provide(provide_user_usecase),
    }
    exception_handlers = {
        UsernameIinvalidLength: handle_invalid_username_length,
        UsernameInvalidSymbol: handle_invalid_username_symbol,
        EmailInvalidStruct: handle_invalid_email_struct,
        UserNotFound: handle_user_not_found,
        DuplicateUserKey: handle_duplicate_user_key,
    }

    @get("/{user_id:uuid}")
    async def get_user(
        self, user_id: UUID, usecase: UserUsecaseProtocol
    ) -> GetUserOutputSchema:
        return await usecase.get_by_id(user_id=user_id)

    @post("/")
    async def create_user(
        self, data: CreateUserInputSchema, usecase: UserUsecaseProtocol
    ) -> None:
        await usecase.create_user(data=data)

    @patch("/{user_id:uuid}")
    async def update_user(
        self, user_id: UUID, data: UpdateUserInputSchema, usecase: UserUsecaseProtocol
    ) -> None:
        await usecase.update_user(user_id=user_id, data=data)

    @delete("/{user_id:uuid}")
    async def delete_user(self, user_id: UUID, usecase: UserUsecaseProtocol) -> None:
        await usecase.delete_user(user_id=user_id)


class PasswordController(Controller):
    path = "/password"
    dependencies = {
        "usecase": Provide(provide_password_usecase),
    }
    exception_handlers = {
        PasswordInvalidLength: handle_invalid_password_length,
        PasswordInvalidSymbol: handle_invalid_password_symbol,
    }

    @post("/{user_id:uuid}")
    async def create_password(
        self,
        user_id: UUID,
        data: CreatePasswordInputSchema,
        usecase: PasswordUsecaseProtocol,
    ) -> None:
        await usecase.create_password(user_id=user_id, data=data)

    @patch("/{user_id:uuid}")
    async def update_password(
        self,
        user_id: UUID,
        data: UpdatePasswordInputSchema,
        usecase: PasswordUsecaseProtocol,
    ) -> None:
        await usecase.update_password(user_id=user_id, data=data)
