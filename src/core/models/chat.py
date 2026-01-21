from datetime import datetime, timezone

from sqlalchemy import DateTime, func, String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.models.base import Base


class Chat(Base):
    title: Mapped[str] = mapped_column(String(200))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
        server_default=func.now(),
        nullable=False,
    )
