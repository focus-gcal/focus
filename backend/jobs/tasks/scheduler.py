from celery import chain, shared_task

from .gcal_integration import create_blocks_in_gcal


@shared_task
def run_scheduler():
    print("Running scheduler algorithm")
    return "scheduler"


@shared_task
def generate_schedule_and_push_to_gcal():
    workflow = chain(
        run_scheduler.s(),
        create_blocks_in_gcal.si(),
    ).apply_async()
    return workflow.id
