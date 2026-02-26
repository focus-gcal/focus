from tasks.models import Task


def get_task_by_id_for_user(user, task_id: int) -> Task | None:
    return Task.objects.filter(user=user, id=task_id).first()
