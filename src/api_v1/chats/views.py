from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.chats import crud
from src.api_v1.chats.schemas import ChatRead, ChatCreate, ChatReadBase
from src.api_v1.messages.schemas import MessageRead
from src.core.models import db_helper

router = APIRouter(tags=['Chats'])


@router.get("/{id}", response_model=ChatRead)
async def get_chat_with_last_messages(
        id: int,
        limit: int = Query(20, ge=1, le=100),
        session: AsyncSession = Depends(db_helper.session_dependency),
):
    chat, messages = await crud.get_chat_with_last_messages(session, id, limit)
    return ChatRead(
        id=chat.id,
        title=chat.title,
        created_at=chat.created_at,
        messages=[MessageRead.model_validate(m) for m in messages],
    )


@router.post('/', response_model=ChatReadBase)
async def create_chat(
        chat: ChatCreate,
        session: AsyncSession = Depends(db_helper.session_dependency)
):
    return await crud.create_chat(session, chat)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat(
        id: int,
        session: AsyncSession = Depends(db_helper.session_dependency),
):
    await crud.delete_chat(session, id)
    return None
