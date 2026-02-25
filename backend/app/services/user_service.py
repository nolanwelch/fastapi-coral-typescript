import uuid

from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.errors import ConflictError, NotFoundError
from app.models.user import User
from app.repositories import user_repo
from app.schemas.user import UserCreate, UserUpdate


async def get_user(session: AsyncSession, user_id: uuid.UUID) -> User:
    user = await user_repo.get(session, user_id)
    if user is None:
        raise NotFoundError(f"User {user_id} not found")
    return user


async def get_all_users(session: AsyncSession) -> list[User]:
    return await user_repo.get_all(session)


async def create_user(session: AsyncSession, data: UserCreate) -> User:
    existing = await user_repo.get_by_email(session, data.email)
    if existing is not None:
        raise ConflictError(f"User with email {data.email} already exists")
    user = User(name=data.name, email=data.email)
    return await user_repo.create(session, user)


async def update_user(
    session: AsyncSession, user_id: uuid.UUID, data: UserUpdate
) -> User:
    user = await get_user(session, user_id)
    update_data = data.model_dump(exclude_unset=True)
    if "email" in update_data:
        existing = await user_repo.get_by_email(session, update_data["email"])
        if existing is not None and existing.id != user_id:
            raise ConflictError(
                f"User with email {update_data['email']} already exists"
            )
    for key, value in update_data.items():
        setattr(user, key, value)
    return await user_repo.update(session, user)


async def delete_user(session: AsyncSession, user_id: uuid.UUID) -> None:
    user = await get_user(session, user_id)
    await user_repo.delete(session, user)
