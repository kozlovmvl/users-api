from http import HTTPStatus
from typing import Any

from litestar import Request, Response
from pydantic import BaseModel
from users_core.validators import (
    EmailInvalidStruct,
    PasswordInvalidLength,
    PasswordInvalidSymbol,
    UsernameIinvalidLength,
    UsernameInvalidSymbol,
)
from users_store.pg.exc import DuplicateUserKey, PasswordNotFound, UserNotFound


class ErrorResponseContent(BaseModel):
    error: str
    args: list[Any]


def handle_user_not_found(_: Request, exc: UserNotFound) -> Response:
    return Response(
        status_code=HTTPStatus.BAD_REQUEST,
        content=ErrorResponseContent(error=exc.__class__.__name__, args=exc.args),
    )


def handle_duplicate_user_key(_: Request, exc: DuplicateUserKey) -> Response:
    return Response(
        status_code=HTTPStatus.BAD_REQUEST,
        content=ErrorResponseContent(error=exc.__class__.__name__, args=exc.args),
    )


def handle_invalid_username_length(_: Request, exc: UsernameIinvalidLength) -> Response:
    return Response(
        status_code=HTTPStatus.BAD_REQUEST,
        content=ErrorResponseContent(error=exc.__class__.__name__, args=exc.args),
    )


def handle_invalid_username_symbol(_: Request, exc: UsernameInvalidSymbol) -> Response:
    return Response(
        status_code=HTTPStatus.BAD_REQUEST,
        content=ErrorResponseContent(error=exc.__class__.__name__, args=exc.args),
    )


def handle_invalid_email_struct(_: Request, exc: EmailInvalidStruct) -> Response:
    return Response(
        status_code=HTTPStatus.BAD_REQUEST,
        content=ErrorResponseContent(error=exc.__class__.__name__, args=exc.args),
    )


def handle_password_not_found(_: Request, exc: PasswordNotFound) -> Response:
    return Response(
        status_code=HTTPStatus.BAD_REQUEST,
        content=ErrorResponseContent(error=exc.__class__.__name__, args=exc.args),
    )


def handle_invalid_password_length(_: Request, exc: PasswordInvalidLength) -> Response:
    return Response(
        status_code=HTTPStatus.BAD_REQUEST,
        content=ErrorResponseContent(error=exc.__class__.__name__, args=exc.args),
    )


def handle_invalid_password_symbol(_: Request, exc: PasswordInvalidSymbol) -> Response:
    return Response(
        status_code=HTTPStatus.BAD_REQUEST,
        content=ErrorResponseContent(error=exc.__class__.__name__, args=exc.args),
    )
