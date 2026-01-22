from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class MessageRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    chat_id: int
    text: str = Field(min_length=1, max_length=5000)
    created_at: datetime


class MessageCreate(BaseModel):
    text: str = Field(min_length=1, max_length=5000)
