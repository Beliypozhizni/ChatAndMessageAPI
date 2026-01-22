from fastapi import APIRouter
from .chats.views import router as chats_router
from .messages.views import router as messages_router

router = APIRouter()
router.include_router(chats_router, prefix="/chats")
router.include_router(messages_router, prefix="/chats/{chat_id}/messages")