from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User


class UsersRepository:
    """Репозиторий для работы с пользователями."""

    def __init__(self, db: AsyncSession):
        self._db = db

    async def get_by_id(self, user_id: int) -> User | None:
        result = await self._db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        result = await self._db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def create(
        self,
        email: str,
        password_hash: str,
        role: str = "user",
    ) -> User:
        user = User(
            email=email,
            password_hash=password_hash,
            role=role,
        )

        self._db.add(user)
        await self._db.commit()
        await self._db.refresh(user)

        return user