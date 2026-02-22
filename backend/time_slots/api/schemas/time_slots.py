from datetime import datetime

from ninja import Schema
from pydantic import field_validator
from tasks.models import Task


class TimeSlotCreateIn(Schema):
    start_time: datetime
    end_time: datetime
    task_id: int | None = None

    @field_validator("start_time")
    @classmethod
    def validate_start_time(cls, v: datetime):
        if v <= datetime.now():
            raise ValueError("Start time must be in the future")
        return v

    @field_validator("end_time")
    @classmethod
    def validate_end_time(cls, v: datetime):
        if v <= datetime.now():
            raise ValueError("End time must be in the future")
        return v

    @field_validator("task_id")
    @classmethod
    def validate_task_id(cls, v: int | None):
        if v is not None and not Task.objects.filter(id=v).exists():
            raise ValueError("Task not found")
        return v


class TimeSlotUpdateIn(Schema):
    start_time: datetime | None = None
    end_time: datetime | None = None
    task_id: int | None = None

    @field_validator("start_time")
    @classmethod
    def validate_start_time(cls, v: datetime | None):
        if v is None:
            return v
        if v <= datetime.now():
            raise ValueError("Start time must be in the future")
        return v

    @field_validator("end_time")
    @classmethod
    def validate_end_time(cls, v: datetime | None):
        if v is None:
            return v
        if v <= datetime.now():
            raise ValueError("End time must be in the future")
        return v

    @field_validator("task_id")
    @classmethod
    def validate_task_id(cls, v: int | None):
        if v is None:
            return v
        if not Task.objects.filter(id=v).exists():
            raise ValueError("Task not found")
        return v


class TimeSlotOut(Schema):
    id: int
    user_id: int
    task_id: int | None
    start_time: datetime
    end_time: datetime
