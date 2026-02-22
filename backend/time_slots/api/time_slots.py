from datetime import datetime

from ninja import Router
from time_slots.models import TimeSlots
from time_slots.selectors.time_slots_selectors import (
    get_time_slot_by_id_for_user,
    get_time_slots_for_user,
)
from time_slots.services.time_slots_services import (
    update_time_slot as update_time_slot_service,
)
from users.auth.ninja_auth import JWTAuth

from .schemas.time_slots import TimeSlotCreateIn, TimeSlotOut, TimeSlotUpdateIn

router = Router()


@router.get("/get_all", response={200: list[TimeSlotOut]}, auth=JWTAuth())
def get_all(request):
    time_slots = get_time_slots_for_user(request.auth)
    return 200, [
        TimeSlotOut(
            id=ts.id,
            user_id=ts.user_id,
            task_id=ts.task_id,
            start_time=ts.start_time,
            end_time=ts.end_time,
        )
        for ts in time_slots
    ]


@router.post("/create", response={200: TimeSlotOut, 400: dict}, auth=JWTAuth())
def create_time_slot(request, data: TimeSlotCreateIn):
    time_slot = TimeSlots(user=request.auth, **data.model_dump())
    try:
        time_slot.full_clean()
        time_slot.save()
    except Exception as e:
        return 400, {"error": str(e)}
    return 200, TimeSlotOut(
        id=time_slot.id,
        user_id=time_slot.user_id,
        task_id=time_slot.task_id,
        start_time=time_slot.start_time,
        end_time=time_slot.end_time,
    )


@router.get(
    "/get/{time_slot_id}", response={200: TimeSlotOut, 404: dict}, auth=JWTAuth()
)
def get_time_slot(request, time_slot_id: int):
    time_slot = get_time_slot_by_id_for_user(request.auth, time_slot_id)
    if time_slot is None:
        return 404, {"error": "Time slot not found."}
    return 200, TimeSlotOut(
        id=time_slot.id,
        user_id=time_slot.user_id,
        task_id=time_slot.task_id,
        start_time=time_slot.start_time,
        end_time=time_slot.end_time,
    )


@router.get(
    "/get_by_start_time_end_time",
    response={200: list[TimeSlotOut], 400: dict},
    auth=JWTAuth(),
)
def get_by_start_time_end_time(request, start_time: datetime, end_time: datetime):
    time_slots = TimeSlots.objects.filter(
        user=request.auth, start_time__gte=start_time, end_time__lte=end_time
    )
    time_slots_list = [
        TimeSlotOut(
            id=ts.id,
            user_id=ts.user_id,
            task_id=ts.task_id,
            start_time=ts.start_time,
            end_time=ts.end_time,
        )
        for ts in time_slots
    ]
    return 200, time_slots_list


@router.delete(
    "/delete/{time_slot_id}", response={200: dict, 404: dict}, auth=JWTAuth()
)
def delete_time_slot(request, time_slot_id: int):
    time_slot = get_time_slot_by_id_for_user(request.auth, time_slot_id)
    if time_slot is None:
        return 404, {"error": "Time slot not found."}
    time_slot.delete()
    return 200, {"message": "Time slot deleted successfully"}


@router.patch(
    "/update/{time_slot_id}",
    response={200: TimeSlotOut, 400: dict, 404: dict},
    auth=JWTAuth(),
)
def update_time_slot(request, time_slot_id: int, data: TimeSlotUpdateIn):
    time_slot, err = update_time_slot_service(request.auth, time_slot_id, data)
    if err:
        status, body = err
        return status, body
    return 200, TimeSlotOut(
        id=time_slot.id,
        user_id=time_slot.user_id,
        task_id=time_slot.task_id,
        start_time=time_slot.start_time,
        end_time=time_slot.end_time,
    )
