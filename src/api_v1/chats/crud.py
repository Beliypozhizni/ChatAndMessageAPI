from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.chats.schemas import ChatCreate
from src.api_v1.messages.crud import get_last_messages
from src.core.models.chat import Chat
from src.core.models.message import Message


async def create_chat(
        session: AsyncSession,
        chat_in: ChatCreate
) -> Chat:
    chat = Chat(**chat_in.model_dump())
    session.add(chat)
    await session.commit()
    await session.refresh(chat)
    return chat


async def get_chat(
        session: AsyncSession,
        chat_id: int
) -> Chat | None:
    stmt = select(Chat).where(Chat.id == chat_id)
    result = await session.execute(stmt)
    chat = result.scalar_one_or_none()
    return chat


async def get_chat_with_last_messages(
        session: AsyncSession,
        chat_id: int,
        limit: int,
) -> tuple[Chat, list[Message]]:
    chat = await get_chat(session, chat_id)

    if chat is not None:
        messages = await get_last_messages(session, chat_id, limit)
        return chat, messages

    raise HTTPException(
        status_code=404,
        detail=f'Chat {chat_id} is not found'
    )


async def delete_chat(session: AsyncSession, chat_id: int) -> None:
    chat = await get_chat(session, chat_id)

    if chat is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chat {chat_id} is not found",
        )

    await session.delete(chat)
    await session.commit()
