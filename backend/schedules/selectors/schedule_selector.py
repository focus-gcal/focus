from schedules.models import Schedule


def get_schedules_for_user(user):
    """Return queryset of schedules for the user, ordered by day, start_time, end_time."""
    return Schedule.objects.filter(user=user).order_by(
        "day_of_week", "start_time", "end_time"
    )


def get_schedule_by_id_for_user(user, schedule_id: int) -> Schedule | None:
    return Schedule.objects.filter(user=user, id=schedule_id).first()
