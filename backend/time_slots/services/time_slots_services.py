from time_slots.models import TimeSlots
from time_slots.selectors.time_slots_selectors import get_time_slot_by_id_for_user


def update_time_slot(
    user, time_slot_id: int, data
) -> tuple[TimeSlots | None, tuple[int, dict] | None]:
    """Returns (time_slot, None) on success, (None, (status_code, body)) on error."""
    time_slot = get_time_slot_by_id_for_user(user, time_slot_id)
    if time_slot is None:
        return None, (404, {"error": "Time slot not found."})
    payload = data.model_dump(exclude_unset=True)
    for key, value in payload.items():
        setattr(time_slot, key, value)
    try:
        time_slot.full_clean()
        time_slot.save()
    except Exception as e:
        return None, (400, {"error": str(e)})
    return time_slot, None
