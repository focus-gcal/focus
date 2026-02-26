from schedules.models import ScheduleTemplate
from tasks.models import Task
from tasks.selectors.task_selector import get_task_by_id_for_user

# If you use a return type for the error tuple:
# UpdateResult = tuple[Task | None, tuple[int, dict] | None]


def update_task(
    user, task_id: int, data
) -> tuple[Task | None, tuple[int, dict] | None]:
    """Returns (task, None) on success, (None, (status_code, body)) on error."""
    task = get_task_by_id_for_user(user, task_id)
    if task is None:
        return None, (404, {"error": "Task not found."})

    payload = data.model_dump(exclude_unset=True)
    if "schedule_name" in payload:
        schedule_name = payload.pop("schedule_name")
        if schedule_name is None:
            task.schedule_id = None
        else:
            template = ScheduleTemplate.objects.filter(
                user=user, name=schedule_name
            ).first()
            if template is None:
                return None, (400, {"error": f"Schedule not found: '{schedule_name}'."})
            task.schedule_id = template.id

    for key, value in payload.items():
        setattr(task, key, value)
    try:
        task.save()
    except Exception as e:
        return None, (400, {"error": str(e)})
    return task, None
