import uuid

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.user import User


async def get(session: AsyncSession, user_id: uuid.UUID) -> User | None:
    return await session.get(User, user_id)


async def get_all(session: AsyncSession) -> list[User]:
    result = await session.exec(select(User))
    return list(result.all())


async def get_by_email(session: AsyncSession, email: str) -> User | None:
    result = await session.exec(select(User).where(User.email == email))
    return result.first()


async def create(session: AsyncSession, user: User) -> User:
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def update(session: AsyncSession, user: User) -> User:
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def delete(session: AsyncSession, user: User) -> None:
    await session.delete(user)
    await session.commit()
