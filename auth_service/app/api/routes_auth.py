from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import get_auth_uc, get_current_user_id
from app.schemas.auth import RegisterRequest, TokenResponse
from app.schemas.user import UserPublic
from app.usecases.auth import AuthUseCase

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    payload: RegisterRequest,
    auth_uc: AuthUseCase = Depends(get_auth_uc),
) -> UserPublic:
    """Регистрирует пользователя."""
    user = await auth_uc.register(
        email=payload.email,
        password=payload.password,
    )
    return UserPublic.model_validate(user)


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
)
async def login(
    form: OAuth2PasswordRequestForm = Depends(),
    auth_uc: AuthUseCase = Depends(get_auth_uc),
) -> TokenResponse:
    """Аутентифицирует пользователя и возвращает JWT."""
    access_token = await auth_uc.login(
        email=form.username,
        password=form.password,
    )
    return TokenResponse(access_token=access_token)


@router.get(
    "/me",
    response_model=UserPublic,
    status_code=status.HTTP_200_OK,
)
async def me(
    user_id: int = Depends(get_current_user_id),
    auth_uc: AuthUseCase = Depends(get_auth_uc),
) -> UserPublic:
    """Возвращает профиль текущего пользователя."""
    user = await auth_uc.me(user_id=user_id)
    return UserPublic.model_validate(user)