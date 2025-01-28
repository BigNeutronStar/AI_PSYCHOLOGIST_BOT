from handlers.handle_generall import router as common_messages_router
from handlers.technique import router as technique_router
from handlers.handlers import router as handlers_router
from aiogram import Router

router = Router()

router.include_router(handlers_router)
router.include_router(technique_router)
router.include_router(common_messages_router)
