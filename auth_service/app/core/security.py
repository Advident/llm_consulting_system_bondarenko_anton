from datetime import UTC, datetime, timedelta

from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Хеширует пароль пользователя."""
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    """Проверяет пароль пользователя по сохранённому хешу."""
    return pwd_context.verify(password, password_hash)


def create_access_token(user_id: int, role: str) -> str:
    """Создаёт JWT access token с обязательными полями."""
    now = datetime.now(UTC)
    expire = now + timedelta(minutes=settings.access_token_expire_minutes)

    payload = {
        "sub": str(user_id),
        "role": role,
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
    }

    return jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm=settings.jwt_alg,
    )


def decode_token(token: str) -> dict:
    """Декодирует и валидирует JWT token."""
    return jwt.decode(
        token,
        settings.jwt_secret,
        algorithms=[settings.jwt_alg],
    )


def is_token_expired_error(exc: Exception) -> bool:
    """Проверяет, связана ли ошибка JWT с истечением срока токена."""
    return isinstance(exc, ExpiredSignatureError)


def is_invalid_token_error(exc: Exception) -> bool:
    """Проверяет, связана ли ошибка с невалидным токеном."""
    return isinstance(exc, JWTError)