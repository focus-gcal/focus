from schedules.models import Schedule, ScheduleTemplate
from schedules.selectors.schedule_selector import get_schedule_template_by_id_for_user


def get_schedule_template_detail(
    user, template_id: int
) -> tuple[ScheduleTemplate | None, tuple[int, dict] | None]:
    """
    Fetch a single schedule template for the user, including its slots and tasks.

    Returns (template, None) on success, (None, (status, body)) on error.
    """
    template = get_schedule_template_by_id_for_user(user, template_id)
    if template is None:
        return None, (404, {"error": "Schedule not found."})
    return template, None


def create_schedule_template(
    user, data
) -> tuple[ScheduleTemplate | None, tuple[int, dict] | None]:
    """
    Create a new schedule template and its time blocks.

    `data` is expected to be a ScheduleCreateIn-like object with
    `.name` and `.blocks` (ScheduleBlockIn instances).
    """
    try:
        template = ScheduleTemplate.objects.create(user=user, name=data.name)
        for block in data.blocks:
            Schedule.objects.create(
                schedule_template=template,
                user=user,
                name=template.name,
                day_of_week=block.day_of_week,
                start_time=block.start_time,
                end_time=block.end_time,
            )
    except Exception as e:
        return None, (400, {"error": str(e)})

    # Reload with slots/tasks prefetch for downstream usage
    template = get_schedule_template_by_id_for_user(user, template.id)
    return template, None


def update_schedule_template(
    user, template_id: int, data
) -> tuple[ScheduleTemplate | None, tuple[int, dict] | None]:
    """
    Update an existing schedule template (name and/or blocks).

    `data` is expected to be a ScheduleUpdateIn-like object with optional
    `.name` and `.blocks` (ScheduleBlockIn instances).
    """
    template = get_schedule_template_by_id_for_user(user, template_id)
    if template is None:
        return None, (404, {"error": "Schedule not found."})

    payload = data.model_dump(exclude_unset=True)

    # Update template name if provided
    name = payload.get("name")
    if name is not None:
        template.name = name

    # Replace blocks if provided
    blocks = payload.get("blocks")
    if blocks is not None:
        # Clear existing slots
        template.slots.all().delete()
        # Recreate slots for each block
        for b in blocks:
            Schedule.objects.create(
                schedule_template=template,
                user=user,
                name=template.name,
                day_of_week=b.day_of_week,
                start_time=b.start_time,
                end_time=b.end_time,
            )

    try:
        template.full_clean()
        template.save()
    except Exception as e:
        return None, (400, {"error": str(e)})

    # Reload with slots/tasks prefetch for downstream usage
    template = get_schedule_template_by_id_for_user(user, template_id)
    return template, None
