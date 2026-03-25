from celery import shared_task


@shared_task
def create_blocks_in_gcal():
    print("Creating blocks in GCal")
    return "create_blocks_in_gcal"
