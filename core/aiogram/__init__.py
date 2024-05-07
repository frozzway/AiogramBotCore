from aiogram import Router

from core.aiogram.handlers import category_router

router = Router(name='aiogram-main-router')
router.include_router(category_router)
