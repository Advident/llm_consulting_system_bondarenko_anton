from collections.abc import AsyncGenerator

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import ExpiredSignatureError, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import InvalidTokenError, TokenExpiredError
from app.core.security import decode_token
from app.db.session import AsyncSessionLocal
from app.repositories.users import UsersRepository
from app.usecases.auth import AuthUseCase

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Выдаёт AsyncSession для работы с БД."""
    async with AsyncSessionLocal() as session:
        yield session


async def get_users_repo(
    db: AsyncSession = Depends(get_db),
) -> UsersRepository:
    """Выдаёт репозиторий пользователей."""
    return UsersRepository(db=db)


async def get_auth_uc(
    users_repo: UsersRepository = Depends(get_users_repo),
) -> AuthUseCase:
    """Выдаёт usecase авторизации."""
    return AuthUseCase(users_repo=users_repo)


async def get_current_user_id(
    token: str = Depends(oauth2_scheme),
) -> int:
    """Извлекает user_id из JWT токена."""
    try:
        payload = decode_token(token)
        sub = payload.get("sub")
        if sub is None:
            raise InvalidTokenError()
        return int(sub)
    except ExpiredSignatureError as exc:
        raise TokenExpiredError() from exc
    except (JWTError, ValueError) as exc:
        raise InvalidTokenError() from exc