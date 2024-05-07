from aiogram import Router

from aiogram_extensions.back_feature import MessageSaverMiddleware
from core.aiogram.handlers.category_handler import category_router

router = Router(name='aiogram-main-router')
router.callback_query.middleware(MessageSaverMiddleware())

# Include handler routers here
router.include_router(category_router)
