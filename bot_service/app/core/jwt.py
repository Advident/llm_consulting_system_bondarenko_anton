from jose import ExpiredSignatureError, JWTError, jwt

from app.core.config import settings


def decode_and_validate(token: str) -> dict:
    """Проверяет JWT, подпись, срок действия и наличие sub."""
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_alg],
        )
    except ExpiredSignatureError as exc:
        raise ValueError("Token has expired") from exc
    except JWTError as exc:
        raise ValueError("Invalid token") from exc

    sub = payload.get("sub")
    if sub is None:
        raise ValueError("Token does not contain sub")

    return payload