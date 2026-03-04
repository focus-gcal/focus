from schedules.models import Schedule, ScheduleTemplate


def get_schedules_for_user(user):
    """
    Return schedule templates for the user, with their slots preloaded.

    Each `ScheduleTemplate` instance has a `.slots` related manager that
    returns its `Schedule` rows (one per day/time block).
    """
    return (
        ScheduleTemplate.objects.filter(user=user)
        .prefetch_related("slots")
        .order_by("name", "id")
    )


def get_schedule_template_by_id_for_user(
    user, template_id: int
) -> ScheduleTemplate | None:
    """
    Fetch a single schedule template for the user, including its slots and tasks.
    """
    return (
        ScheduleTemplate.objects.filter(user=user, id=template_id)
        .prefetch_related("slots", "tasks")
        .first()
    )


def get_schedule_by_id_for_user(user, schedule_id: int) -> Schedule | None:
    return Schedule.objects.filter(user=user, id=schedule_id).first()
