from aiogram import Router

from core.aiogram.handlers.category_handler import category_router

router = Router(name='aiogram-main-router')

# Include handler routers here
router.include_router(category_router)
