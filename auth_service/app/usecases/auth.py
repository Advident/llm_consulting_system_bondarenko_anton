from app.core.exceptions import (
    InvalidCredentialsError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from app.core.security import create_access_token, hash_password, verify_password
from app.db.models import User
from app.repositories.users import UsersRepository


class AuthUseCase:
    """Бизнес-логика регистрации, логина и получения профиля."""

    def __init__(self, users_repo: UsersRepository) -> None:
        self._users_repo = users_repo

    async def register(self, email: str, password: str) -> User:
        """Регистрирует нового пользователя."""
        existing_user = await self._users_repo.get_by_email(email)
        if existing_user is not None:
            raise UserAlreadyExistsError()

        password_hash = hash_password(password)
        return await self._users_repo.create(
            email=email,
            password_hash=password_hash,
            role="user",
        )

    async def login(self, email: str, password: str) -> str:
        """Проверяет учётные данные и возвращает JWT."""
        user = await self._users_repo.get_by_email(email)
        if user is None:
            raise InvalidCredentialsError()

        if not verify_password(password, user.password_hash):
            raise InvalidCredentialsError()

        return create_access_token(user_id=user.id, role=user.role)

    async def me(self, user_id: int) -> User:
        """Возвращает текущего пользователя по id."""
        user = await self._users_repo.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError()

        return user