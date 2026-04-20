from datetime import UTC, datetime, timedelta

import pytest
from jose import jwt

from app.core.config import settings
from app.core.jwt import decode_and_validate


def create_test_token(
    sub: str = "1",
    role: str = "user",
    expires_delta_minutes: int = 60,
) -> str:
    """Создаёт тестовый JWT тем же секретом, что и Bot Service."""
    now = datetime.now(UTC)
    expire = now + timedelta(minutes=expires_delta_minutes)

    payload = {
        "sub": sub,
        "role": role,
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
    }

    return jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm=settings.jwt_alg,
    )


def test_decode_and_validate_success():
    token = create_test_token(sub="123", role="user")

    payload = decode_and_validate(token)

    assert payload["sub"] == "123"
    assert payload["role"] == "user"
    assert "iat" in payload
    assert "exp" in payload


def test_decode_and_validate_invalid_token():
    with pytest.raises(ValueError, match="Invalid token"):
        decode_and_validate("not-a-real-jwt")


def test_decode_and_validate_expired_token():
    token = create_test_token(expires_delta_minutes=-1)

    with pytest.raises(ValueError, match="Token has expired"):
        decode_and_validate(token)