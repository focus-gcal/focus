from time_slots.models import TimeSlots


def get_time_slots_for_user(user):
    """Return queryset of time slots for the user, ordered by start_time and end_time."""
    return TimeSlots.objects.filter(user=user).order_by("start_time", "end_time")


def get_time_slot_by_id_for_user(user, time_slot_id: int) -> TimeSlots | None:
    return TimeSlots.objects.filter(user=user, id=time_slot_id).first()
