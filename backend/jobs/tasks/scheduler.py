from datetime import datetime, time, timedelta

from celery import chain, shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone
from tasks.models import Task
from time_slots.models import TimeSlots

from .gcal_integration import create_blocks_in_gcal


@shared_task
def run_scheduler(user_id: int):
    print("Running scheduler algorithm")
    user = get_user_model().objects.get(id=user_id)
    today = timezone.localdate()
    tomorrow = today + timedelta(days=1)
    tz = timezone.get_current_timezone()

    def slot_dt(day, hour: int, minute: int):
        return timezone.make_aware(
            datetime.combine(day, time(hour=hour, minute=minute)),
            tz,
        )

    # Delete all existing slots for this user before creating new ones.
    TimeSlots.objects.filter(user=user).delete()

    mock_task_titles = [
        "Morning Deep Work",
        "Project Sprint",
        "Email + Admin",
        "Learning Block",
        "Review + Planning",
    ]
    task_pool = []
    for title in mock_task_titles:
        task, _ = Task.objects.get_or_create(
            user=user,
            title=title,
            defaults={"duration": 60},
        )
        task_pool.append(task)

    slot_specs = {
        today: [
            (8, 0, 9, 0),
            (9, 30, 11, 0),
            (11, 30, 12, 30),
            (14, 0, 15, 0),
            (15, 30, 17, 0),
        ],
        tomorrow: [
            (8, 30, 9, 30),
            (10, 0, 11, 30),
            (13, 0, 14, 0),
            (14, 30, 15, 30),
            (16, 0, 17, 0),
        ],
    }

    created_slots = []
    for day, windows in slot_specs.items():
        for start_h, start_m, end_h, end_m in windows:
            slot_duration = ((end_h * 60) + end_m) - ((start_h * 60) + start_m)
            task = task_pool[len(created_slots) % len(task_pool)]
            if task.duration != slot_duration:
                task.duration = slot_duration
                task.save(update_fields=["duration"])

            slot = TimeSlots(
                user=user,
                task=task,
                start_time=slot_dt(day, start_h, start_m),
                end_time=slot_dt(day, end_h, end_m),
            )
            slot.full_clean()
            slot.save()
            created_slots.append(
                {
                    "id": slot.id,
                    "task_id": slot.task_id,
                    "task_title": slot.task.title if slot.task else None,
                    "start_time": slot.start_time.isoformat(),
                    "end_time": slot.end_time.isoformat(),
                }
            )

    return {"user_id": user_id, "created_slots": created_slots}


@shared_task
def generate_schedule_and_push_to_gcal(user_id: int):
    workflow = chain(
        run_scheduler.s(user_id),
        create_blocks_in_gcal.si(user_id),
    ).apply_async()
    return workflow.id
