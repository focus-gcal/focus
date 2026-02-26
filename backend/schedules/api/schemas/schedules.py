from datetime import time

from ninja import Schema
from pydantic import field_validator


class ScheduleCreateIn(Schema):
    name: str
    day_of_week: int
    start_time: time
    end_time: time

    @field_validator("name")
    @classmethod
    def clean_name(cls, v: str):
        v = v.strip()
        if not v:
            raise ValueError("name cannot be blank")
        if len(v) > 100:
            raise ValueError("name must be at most 100 characters")
        return v

    @field_validator("day_of_week")
    @classmethod
    def valid_day(cls, v: int):
        if v not in (0, 1, 2, 3, 4, 5, 6):
            raise ValueError("day_of_week must be 0 (Mon) through 6 (Sun)")
        return v

    @field_validator("end_time")
    @classmethod
    def end_after_start(cls, v: time, info):
        start = info.data.get("start_time")
        if start is not None and v <= start:
            raise ValueError("end_time must be after start_time")
        return v


class ScheduleUpdateIn(Schema):
    """Partial payload for updating a schedule; all fields optional."""

    name: str | None = None
    day_of_week: int | None = None
    start_time: time | None = None
    end_time: time | None = None

    @field_validator("name")
    @classmethod
    def clean_name(cls, v: str | None):
        if v is None:
            return v
        v = v.strip()
        if not v:
            raise ValueError("name cannot be blank")
        if len(v) > 100:
            raise ValueError("name must be at most 100 characters")
        return v

    @field_validator("day_of_week")
    @classmethod
    def valid_day(cls, v: int | None):
        if v is not None and v not in (0, 1, 2, 3, 4, 5, 6):
            raise ValueError("day_of_week must be 0 (Mon) through 6 (Sun)")
        return v

    @field_validator("end_time")
    @classmethod
    def end_after_start(cls, v: time | None, info):
        if v is None:
            return v
        start = info.data.get("start_time")
        if start is not None and v <= start:
            raise ValueError("end_time must be after start_time")
        return v


class ScheduleTaskOut(Schema):
    """Minimal task info returned with a schedule (tasks assigned to this schedule's template)."""

    id: int
    title: str


class ScheduleOut(Schema):
    id: int
    user_id: int
    name: str
    day_of_week: int
    start_time: time
    end_time: time


class ScheduleListOut(Schema):
    """Schedule including the list of tasks assigned to its template."""

    id: int
    user_id: int
    name: str
    day_of_week: int
    start_time: time
    end_time: time
    tasks: list[ScheduleTaskOut] = []
