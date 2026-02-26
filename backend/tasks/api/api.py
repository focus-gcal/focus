from ninja import Router

from .tasks import router as tasks_router

router = Router()
router.add_router("", tasks_router)
