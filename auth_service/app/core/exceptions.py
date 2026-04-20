from fastapi import HTTPException, status


class BaseHTTPException(HTTPException):
    """Базовое HTTP-исключение приложения."""

    def __init__(self, status_code: int, detail: str) -> None:
        super().__init__(status_code=status_code, detail=detail)


class UserAlreadyExistsError(BaseHTTPException):
    """Пользователь с таким email уже существует."""

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )


class InvalidCredentialsError(BaseHTTPException):
    """Неверный email или пароль."""

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )


class InvalidTokenError(BaseHTTPException):
    """Токен невалиден."""

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )


class TokenExpiredError(BaseHTTPException):
    """Срок действия токена истёк."""

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )


class UserNotFoundError(BaseHTTPException):
    """Пользователь не найден."""

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )


class PermissionDeniedError(BaseHTTPException):
    """Недостаточно прав."""

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied",
        )