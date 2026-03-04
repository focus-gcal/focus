from datetime import time

from ninja import Schema
from pydantic import field_validator


class ScheduleCreateIn(Schema):
    """
    Create a logical schedule template with its time blocks.
    """

    name: str
    blocks: list["ScheduleBlockIn"]

    @field_validator("name")
    @classmethod
    def clean_name(cls, v: str):
        v = v.strip()
        if not v:
            raise ValueError("name cannot be blank")
        if len(v) > 100:
            raise ValueError("name must be at most 100 characters")
        return v

    @field_validator("blocks")
    @classmethod
    def validate_blocks(cls, v: list["ScheduleBlockIn"]):
        if not v:
            raise ValueError("blocks must not be empty")
        return v


class ScheduleUpdateIn(Schema):
    """
    Update a schedule template; all fields optional.

    If `blocks` is provided, it replaces the entire set of time blocks.
    """

    name: str | None = None
    blocks: list["ScheduleBlockIn"] | None = None

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


class ScheduleTaskOut(Schema):
    """Minimal task info returned with a schedule (tasks assigned to this schedule's template)."""

    id: int
    title: str


class ScheduleBlockIn(Schema):
    """Input shape for a time block (day + time range)."""

    day_of_week: int
    start_time: time
    end_time: time

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


class ScheduleBlockOut(Schema):
    """One concrete time block for a template (day + time range)."""

    day_of_week: int
    start_time: time
    end_time: time


class ScheduleTemplateOut(Schema):
    """
    Logical schedule template (e.g. 'Work') with all of its time blocks.

    This is what GET /schedules/ will return so the frontend can treat each
    template as a single schedule with multiple ranges.
    """

    id: int
    user_id: int
    name: str
    blocks: list[ScheduleBlockOut]


class ScheduleTemplateDetailOut(ScheduleTemplateOut):
    """Template with its blocks and the tasks assigned to it."""

    tasks: list[ScheduleTaskOut] = []
