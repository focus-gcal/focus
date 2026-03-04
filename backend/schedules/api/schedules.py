from ninja import Router
from schedules.selectors.schedule_selector import get_schedules_for_user
from schedules.services import schedule_services
from users.auth.ninja_auth import JWTAuth

from .schemas.schedules import (
    ScheduleBlockOut,
    ScheduleCreateIn,
    ScheduleTaskOut,
    ScheduleTemplateDetailOut,
    ScheduleTemplateOut,
    ScheduleUpdateIn,
)

router = Router()


@router.get("/", response={200: list[ScheduleTemplateOut]}, auth=JWTAuth())
def list_schedules(request):
    """
    Return one item per schedule template for the user, each with its blocks.
    """
    templates = get_schedules_for_user(request.auth)
    return 200, [
        ScheduleTemplateOut(
            id=t.id,
            user_id=t.user_id,
            name=t.name,
            blocks=[
                ScheduleBlockOut(
                    day_of_week=slot.day_of_week,
                    start_time=slot.start_time,
                    end_time=slot.end_time,
                )
                for slot in sorted(
                    t.slots.all(),
                    key=lambda s: (s.day_of_week, s.start_time, s.end_time),
                )
            ],
        )
        for t in templates
    ]


@router.get(
    "/{schedule_id}",
    response={200: ScheduleTemplateDetailOut, 404: dict},
    auth=JWTAuth(),
)
def get_schedule(request, schedule_id: int):
    """
    Return a single schedule template (by id) with all its blocks and tasks.
    """
    template, err = schedule_services.get_schedule_template_detail(
        request.auth, schedule_id
    )
    if err:
        status, body = err
        return status, body

    blocks = [
        ScheduleBlockOut(
            day_of_week=slot.day_of_week,
            start_time=slot.start_time,
            end_time=slot.end_time,
        )
        for slot in sorted(
            template.slots.all(),
            key=lambda s: (s.day_of_week, s.start_time, s.end_time),
        )
    ]

    tasks = [ScheduleTaskOut(id=t.id, title=t.title) for t in template.tasks.all()]

    return 200, ScheduleTemplateDetailOut(
        id=template.id,
        user_id=template.user_id,
        name=template.name,
        blocks=blocks,
        tasks=tasks,
    )


@router.delete("/{schedule_id}", response={200: dict, 404: dict}, auth=JWTAuth())
def delete_schedule(request, schedule_id: int):
    template, err = schedule_services.get_schedule_template_detail(
        request.auth, schedule_id
    )
    if err:
        status, body = err
        return status, body
    template.delete()
    return 200, {"message": "Schedule deleted successfully."}


@router.patch(
    "/{schedule_id}",
    response={200: ScheduleTemplateDetailOut, 400: dict, 404: dict},
    auth=JWTAuth(),
)
def update_schedule(request, schedule_id: int, data: ScheduleUpdateIn):
    template, err = schedule_services.update_schedule_template(
        request.auth, schedule_id, data
    )
    if err:
        status, body = err
        return status, body

    blocks_out = [
        ScheduleBlockOut(
            day_of_week=slot.day_of_week,
            start_time=slot.start_time,
            end_time=slot.end_time,
        )
        for slot in sorted(
            template.slots.all(),
            key=lambda s: (s.day_of_week, s.start_time, s.end_time),
        )
    ]

    tasks = [ScheduleTaskOut(id=t.id, title=t.title) for t in template.tasks.all()]

    return 200, ScheduleTemplateDetailOut(
        id=template.id,
        user_id=template.user_id,
        name=template.name,
        blocks=blocks_out,
        tasks=tasks,
    )


@router.post("/", response={200: ScheduleTemplateDetailOut, 400: dict}, auth=JWTAuth())
def create_schedule(request, data: ScheduleCreateIn):
    template, err = schedule_services.create_schedule_template(request.auth, data)
    if err:
        status, body = err
        return status, body

    blocks_out = [
        ScheduleBlockOut(
            day_of_week=slot.day_of_week,
            start_time=slot.start_time,
            end_time=slot.end_time,
        )
        for slot in sorted(
            template.slots.all(),
            key=lambda s: (s.day_of_week, s.start_time, s.end_time),
        )
    ]

    tasks = [ScheduleTaskOut(id=t.id, title=t.title) for t in template.tasks.all()]

    return 200, ScheduleTemplateDetailOut(
        id=template.id,
        user_id=template.user_id,
        name=template.name,
        blocks=blocks_out,
        tasks=tasks,
    )
