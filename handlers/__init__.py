from aiogram import Router
from .start import router as start_router
from .mood import router as mood_router
from .relaxation import router as relaxation_router
from .support import router as support_router
from .self_help import router as self_help_router

router = Router()
router.include_router(start_router)
router.include_router(mood_router)
router.include_router(relaxation_router)
router.include_router(support_router)
router.include_router(self_help_router)