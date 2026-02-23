from ninja import NinjaAPI

from schedules.api import api as schedules_api
from tasks.api import api as tasks_api
from time_slots.api import api as time_slots_api

from users.api import api as users_api
from users.api import api as auth_api

api = NinjaAPI()

api.add_router("/auth/", auth_api.router)
api.add_router("/users/", users_api.router)
api.add_router("/schedules/", schedules_api.router)
api.add_router("/time_slots/", time_slots_api.router)
api.add_router("/tasks/", tasks_api.router)


@api.get("/ping")
def ping(request):
    return "pong"