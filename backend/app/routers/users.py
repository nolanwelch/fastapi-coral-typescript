import uuid

from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.dependencies import get_session
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.services import user_service

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserRead])
async def list_users(
    session: AsyncSession = Depends(get_session),
) -> list[UserRead]:
    users = await user_service.get_all_users(session)
    return [UserRead.model_validate(u) for u in users]


@router.get("/{user_id}", response_model=UserRead)
async def get_user(
    user_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
) -> UserRead:
    user = await user_service.get_user(session, user_id)
    return UserRead.model_validate(user)


@router.post("/", response_model=UserRead, status_code=201)
async def create_user(
    data: UserCreate,
    session: AsyncSession = Depends(get_session),
) -> UserRead:
    user = await user_service.create_user(session, data)
    return UserRead.model_validate(user)


@router.patch("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: uuid.UUID,
    data: UserUpdate,
    session: AsyncSession = Depends(get_session),
) -> UserRead:
    user = await user_service.update_user(session, user_id, data)
    return UserRead.model_validate(user)


@router.delete("/{user_id}", status_code=204)
async def delete_user(
    user_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
) -> None:
    await user_service.delete_user(session, user_id)
