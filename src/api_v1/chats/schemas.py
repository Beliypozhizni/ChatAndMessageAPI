from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict, Field

from src.api_v1.messages.schemas import MessageRead


class ChatReadBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str = Field(max_length=200)
    created_at: datetime


class ChatRead(ChatReadBase):
    messages: List[MessageRead] = Field(default_factory=list)


class ChatCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
