from collections.abc import Iterable

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from time_slots.models import GoogleCalendarEvent, TimeSlots
from time_slots.selectors.gcal_selectors import (
    get_gcal_events_by_event_ids_for_user,
    get_today_future_gcal_events_for_user,
)
from users.models import User


class GoogleCalendar:
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.creds = Credentials(token=access_token)
        self.service = build("calendar", "v3", credentials=self.creds)

    def create_calendar(self):
        created = (
            self.service.calendars()
            .insert(
                body={
                    "summary": "Focus Tasks",
                    "description": "Your Focus calendar for planned tasks and time blocks.",
                }
            )
            .execute()
        )
        return created

    def delete_outdated_events(self, user: User):
        events = get_today_future_gcal_events_for_user(user)
        deleted_event_ids = []

        def batch_delete_callback(request_id, response, exception):
            if exception is None:
                deleted_event_ids.append(request_id)
            else:
                print(f"Error deleting event {request_id}: {exception}")

        batch = self.service.new_batch_http_request(callback=batch_delete_callback)
        for event in events:
            batch.add(
                self.service.events().delete(
                    calendarId=user.gcal_calendar_id, eventId=event.event_id
                ),
                request_id=event.event_id,
            )
        batch.execute()
        get_gcal_events_by_event_ids_for_user(user, deleted_event_ids).delete()

    def create_events(self, time_slots: Iterable[TimeSlots]):
        slot_by_request_id: dict[str, TimeSlots] = {}
        successful: list[tuple[str, str]] = []

        def batch_create_callback(request_id, response, exception):
            if exception is None and response and response.get("id"):
                successful.append((request_id, response["id"]))
            else:
                print(f"Error creating event {request_id}: {exception}")
                raise exception

        batch = self.service.new_batch_http_request(callback=batch_create_callback)

        for time_slot in time_slots:
            req_id = str(time_slot.id)
            slot_by_request_id[req_id] = time_slot
            task = time_slot.task
            request = self.service.events().insert(
                calendarId=time_slot.user.gcal_calendar_id,
                body={
                    "start": {
                        "dateTime": time_slot.start_time.isoformat(),
                        "timeZone": "UTC",
                    },
                    "end": {
                        "dateTime": time_slot.end_time.isoformat(),
                        "timeZone": "UTC",
                    },
                    "summary": task.title if task else "Unnamed Task",
                    "description": task.description if task else "",
                },
            )
            batch.add(request, request_id=req_id)
        batch.execute()
        rows = []
        for req_id, google_event_id in successful:
            slot = slot_by_request_id[req_id]
            task = slot.task
            rows.append(
                GoogleCalendarEvent(
                    user=slot.user,
                    event_id=google_event_id,
                    start_time=slot.start_time,
                    end_time=slot.end_time,
                    summary=task.title if task else "Unnamed Task",
                    description=task.description if task else "",
                )
            )
        if rows:
            GoogleCalendarEvent.objects.bulk_create(rows)
