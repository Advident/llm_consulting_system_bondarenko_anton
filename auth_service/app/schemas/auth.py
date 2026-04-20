from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    """Запрос на регистрацию пользователя."""

    email: EmailStr
    password: str = Field(min_length=6, max_length=128)


class TokenResponse(BaseModel):
    """Ответ с JWT токеном."""

    access_token: str
    token_type: str = "bearer"