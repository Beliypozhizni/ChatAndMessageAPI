from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.messages.schemas import MessageCreate
from src.core.models.message import Message
from src.utils.logger import logger


async def create_message(
        session: AsyncSession,
        chat_id: int,
        message_in: MessageCreate
) -> Message:
    message = Message(chat_id=chat_id, **message_in.model_dump())
    session.add(message)
    await session.commit()
    await session.refresh(message)
    logger.info(f"Message created: id={message.id} chat_id={message.chat_id} text_len={len(message.text)}")
    return message


async def get_last_messages(
        session: AsyncSession,
        chat_id: int,
        limit: int,
) -> list[Message]:
    stmt = (
        select(Message)
        .where(Message.chat_id == chat_id)
        .order_by(Message.created_at.desc())
        .limit(limit)
    )

    result = await session.execute(stmt)
    messages = result.scalars().all()

    return list(reversed(messages))
