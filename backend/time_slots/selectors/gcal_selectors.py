from django.db.models import QuerySet
from django.utils import timezone
from time_slots.models import GoogleCalendarEvent


def get_today_future_gcal_events_for_user(
    user,
) -> QuerySet[GoogleCalendarEvent]:
    """Events for the user's current day that have not started yet."""
    current = timezone.now()
    return GoogleCalendarEvent.objects.filter(
        user=user,
        start_time__gt=current,
    )


def get_gcal_events_by_event_ids_for_user(
    user,
    event_ids: list[str],
) -> QuerySet[GoogleCalendarEvent]:
    """Events matching Google event IDs for this user."""
    return GoogleCalendarEvent.objects.filter(
        user=user,
        event_id__in=event_ids,
    )
