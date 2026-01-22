from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.chats import crud as chats_crud
from src.api_v1.messages import crud as messages_crud
from src.api_v1.messages.schemas import MessageRead, MessageCreate
from src.core.models import db_helper

router = APIRouter(tags=['Messages'])


@router.post("/", response_model=MessageRead, status_code=status.HTTP_201_CREATED)
async def create_message(
        chat_id: int,
        body: MessageCreate,
        session: AsyncSession = Depends(db_helper.session_dependency),
):
    chat = await chats_crud.get_chat(session, chat_id)
    if chat is None:
        raise HTTPException(status_code=404, detail=f"Chat {chat_id} is not found")

    message = await messages_crud.create_message(session, chat_id, body)
    return message
