from django.contrib.auth.hashers import make_password
from django.db import transaction
from users.auth.google import GoogleCredentials, GoogleUserInfo
from users.models import User
from utils.gcal import GoogleCalendar


class UserRepository:
    @staticmethod
    @transaction.atomic
    def get_or_create_user_from_google(
        user_info: GoogleUserInfo, credentials: GoogleCredentials
    ):
        user = User.objects.filter(google_sub=user_info.sub).first()
        if user is None:
            gcal = GoogleCalendar(credentials.access_token)
            created = gcal.create_calendar()
            gcal_calendar_id = created.get("id")
            user = User.objects.create(
                email=user_info.email,
                google_sub=user_info.sub,
                first_name=user_info.name,
                refresh_token=credentials.refresh_token,
                password=make_password(None),
                is_active=True,
                is_staff=False,
                is_superuser=False,
                gcal_calendar_id=gcal_calendar_id,
            )

            return user

        changed = False
        if (
            user.refresh_token != credentials.refresh_token and credentials.refresh_token is not None  # fmt: skip
        ):
            user.refresh_token = credentials.refresh_token
            changed = True
        if user.first_name != user_info.name:
            user.first_name = user_info.name
            changed = True
        if user.email != user_info.email:
            user.email = user_info.email
            changed = True
        if changed:
            user.save()
        return user
