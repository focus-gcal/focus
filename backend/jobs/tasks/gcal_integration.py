from celery import shared_task
from users.auth.google import GoogleAuthService
from users.models import User
from utils.gcal import GoogleCalendar


@shared_task
def create_blocks_in_gcal(user_id: int):
    user = User.objects.prefetch_related("blocks", "tasks").get(id=user_id)
    access_token = GoogleAuthService.get_valid_access_token(user_id)
    gcal = GoogleCalendar(access_token)
    gcal.delete_outdated_events(user)
    gcal.create_events(user.blocks.all())
    # create new blocks in gcal for next 2 days (time slot contains what scheduler generated)
