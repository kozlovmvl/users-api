from uuid import UUID

from pydantic import BaseModel, ConfigDict


class GetUserOutputSchema(BaseModel):
    id: UUID
    username: str
    email: str

    model_config = ConfigDict(from_attributes=True)


class CreateUserInputSchema(BaseModel):
    username: str
    email: str


class UpdateUserInputSchema(BaseModel):
    email: str | None = None


class CreatePasswordInputSchema(BaseModel):
    value: str


class UpdatePasswordInputSchema(BaseModel):
    current: str
    new: str
