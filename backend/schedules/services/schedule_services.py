from schedules.models import Schedule
from schedules.selectors.schedule_selector import get_schedule_by_id_for_user


def get_schedule_tasks(schedule: Schedule) -> list[dict]:
    """Return tasks assigned to this schedule's template. Each item is {"id": int, "title": str}."""
    if not schedule.schedule_template_id:
        return []
    return [
        {"id": t.id, "title": t.title} for t in schedule.schedule_template.tasks.all()
    ]


def update_schedule(
    user, schedule_id: int, data
) -> tuple[Schedule | None, tuple[int, dict] | None]:
    """Returns (schedule, None) on success, (None, (status_code, body)) on error."""
    schedule = get_schedule_by_id_for_user(user, schedule_id)
    if schedule is None:
        return None, (404, {"error": "Schedule not found."})

    payload = data.model_dump(exclude_unset=True)
    for key, value in payload.items():
        setattr(schedule, key, value)
    try:
        schedule.full_clean()
        schedule.save()
    except Exception as e:
        return None, (400, {"error": str(e)})
    return schedule, None
