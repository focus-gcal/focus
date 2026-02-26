from ninja import Router

from .time_slots import router as time_slots_router

router = Router()
router.add_router("", time_slots_router)
