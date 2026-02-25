import uuid
from datetime import datetime

from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    email: str


class UserRead(BaseModel):
    id: uuid.UUID
    name: str
    email: str
    created_at: datetime

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
