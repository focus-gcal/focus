from ninja import Router
from schedules.models import Schedule, ScheduleTemplate
from schedules.selectors.schedule_selector import (
    get_schedule_by_id_for_user,
    get_schedules_for_user,
)
from schedules.services import schedule_services
from users.auth.ninja_auth import JWTAuth

from .schemas.schedules import (
    ScheduleCreateIn,
    ScheduleOut,
    ScheduleTaskOut,
    ScheduleUpdateIn,
)

router = Router()


@router.get("/get_all", response={200: list[ScheduleOut]}, auth=JWTAuth())
def get_all(request):
    schedules = get_schedules_for_user(request.auth).prefetch_related(
        "schedule_template__tasks"
    )
    return 200, [
        ScheduleOut(
            id=s.id,
            user_id=s.user_id,
            name=s.name,
            day_of_week=s.day_of_week,
            start_time=s.start_time,
            end_time=s.end_time,
            tasks=[
                ScheduleTaskOut(**t) for t in schedule_services.get_schedule_tasks(s)
            ],
        )
        for s in schedules
    ]


@router.get(
    "/get/{schedule_id}", response={200: ScheduleOut, 404: dict}, auth=JWTAuth()
)
def get_schedule(request, schedule_id: int):
    schedule = get_schedule_by_id_for_user(request.auth, schedule_id)
    if schedule is None:
        return 404, {"error": "Schedule not found."}
    return 200, ScheduleOut(
        id=schedule.id,
        user_id=schedule.user_id,
        name=schedule.name,
        day_of_week=schedule.day_of_week,
        start_time=schedule.start_time,
        end_time=schedule.end_time,
        tasks=[
            ScheduleTaskOut(**t) for t in schedule_services.get_schedule_tasks(schedule)
        ],
    )


@router.delete("/delete/{schedule_id}", response={200: dict, 404: dict}, auth=JWTAuth())
def delete_schedule(request, schedule_id: int):
    schedule = get_schedule_by_id_for_user(request.auth, schedule_id)
    if schedule is None:
        return 404, {"error": "Schedule not found."}
    schedule.delete()
    return 200, {"message": "Schedule deleted successfully."}


@router.patch(
    "/update/{schedule_id}",
    response={200: ScheduleOut, 400: dict, 404: dict},
    auth=JWTAuth(),
)
def update_schedule(request, schedule_id: int, data: ScheduleUpdateIn):
    schedule, err = schedule_services.update_schedule(request.auth, schedule_id, data)
    if err:
        status, body = err
        return status, body
    return 200, ScheduleOut(
        id=schedule.id,
        user_id=schedule.user_id,
        name=schedule.name,
        day_of_week=schedule.day_of_week,
        start_time=schedule.start_time,
        end_time=schedule.end_time,
        tasks=[
            ScheduleTaskOut(**t) for t in schedule_services.get_schedule_tasks(schedule)
        ],
    )


@router.post("/create", response={200: ScheduleOut, 400: dict}, auth=JWTAuth())
def create(request, data: ScheduleCreateIn):
    try:
        template, _ = ScheduleTemplate.objects.get_or_create(
            user=request.auth, name=data.name
        )
        schedule = Schedule.objects.create(
            schedule_template=template,
            user=request.auth,
            name=template.name,
            day_of_week=data.day_of_week,
            start_time=data.start_time,
            end_time=data.end_time,
        )
    except Exception as e:
        return 400, {"error": str(e)}
    return 200, ScheduleOut(
        id=schedule.id,
        user_id=schedule.user_id,
        name=schedule.name,
        day_of_week=schedule.day_of_week,
        start_time=schedule.start_time,
        end_time=schedule.end_time,
        tasks=[
            ScheduleTaskOut(**t) for t in schedule_services.get_schedule_tasks(schedule)
        ],
    )
