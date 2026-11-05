from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from users.schemas import UserResponse


class PostBase(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=1, max_length=1000)
    author: str = Field(min_length=1, max_length=50)


class PostCreate(PostBase):
    user_id: int


class PostResponse(PostBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    date_posted: datetime
    author: UserResponse
