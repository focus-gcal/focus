from ninja import Router

from .schedules import router as schedules_router

router = Router()
router.add_router("", schedules_router)
