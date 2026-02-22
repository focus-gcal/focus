from datetime import datetime

from ninja import Schema
from pydantic import field_validator
from tasks.models import TaskPriority, TaskStatus


class TaskCreateIn(Schema):
    title: str
    description: str = ""
    duration: int
    priority: int = TaskPriority.LOW
    deadline: datetime | None = None
    is_hard_deadline: bool = False
    status: str = TaskStatus.TODO
    start_date: datetime | None = None
    min_chunk: int | None = None
    max_duration_chunk: int | None = None
    schedule_name: str | None = None

    @field_validator("title")
    @classmethod
    def clean_title(cls, v: str):
        v = v.strip()
        if not v:
            raise ValueError("title cannot be blank")
        if len(v) > 200:
            raise ValueError("title must be at most 200 characters")
        return v

    @field_validator("duration")
    @classmethod
    def duration_positive(cls, v: int):
        if v <= 0:
            raise ValueError("duration must be positive")
        return v

    @field_validator("priority")
    @classmethod
    def valid_priority(cls, v: int):
        if v not in (TaskPriority.LOW, TaskPriority.MEDIUM, TaskPriority.HIGH):
            raise ValueError("priority must be 1 (Low), 2 (Medium), or 3 (High)")
        return v

    @field_validator("status")
    @classmethod
    def valid_status(cls, v: str):
        allowed = [s.value for s in TaskStatus]
        if v not in allowed:
            raise ValueError(f"status must be one of: {', '.join(allowed)}")
        return v

    @field_validator("min_chunk")
    @classmethod
    def min_chunk_positive(cls, v: int | None):
        if v is not None and v <= 0:
            raise ValueError("min_chunk must be positive when provided")
        return v

    @field_validator("max_duration_chunk")
    @classmethod
    def max_duration_chunk_positive(cls, v: int | None):
        if v is not None and v <= 0:
            raise ValueError("max_duration_chunk must be positive when provided")
        return v

    @field_validator("schedule_name")
    @classmethod
    def clean_schedule_name(cls, v: str | None):
        if v is None:
            return v
        v = v.strip()
        if not v:
            raise ValueError("schedule_name cannot be blank")
        return v


class TaskUpdateIn(Schema):
    """Partial payload for updating a task; all fields optional."""

    title: str | None = None
    description: str | None = None
    duration: int | None = None
    priority: int | None = None
    deadline: datetime | None = None
    is_hard_deadline: bool | None = None
    status: str | None = None
    start_date: datetime | None = None
    min_chunk: int | None = None
    max_duration_chunk: int | None = None
    schedule_name: str | None = None

    @field_validator("title")
    @classmethod
    def clean_title(cls, v: str | None):
        if v is None:
            return v
        v = v.strip()
        if not v:
            raise ValueError("title cannot be blank")
        if len(v) > 200:
            raise ValueError("title must be at most 200 characters")
        return v

    @field_validator("duration")
    @classmethod
    def duration_positive(cls, v: int | None):
        if v is not None and v <= 0:
            raise ValueError("duration must be positive")
        return v

    @field_validator("priority")
    @classmethod
    def valid_priority(cls, v: int | None):
        if v is not None and v not in (
            TaskPriority.LOW,
            TaskPriority.MEDIUM,
            TaskPriority.HIGH,
        ):
            raise ValueError("priority must be 1 (Low), 2 (Medium), or 3 (High)")
        return v

    @field_validator("status")
    @classmethod
    def valid_status(cls, v: str | None):
        if v is None:
            return v
        allowed = [s.value for s in TaskStatus]
        if v not in allowed:
            raise ValueError(f"status must be one of: {', '.join(allowed)}")
        return v

    @field_validator("min_chunk")
    @classmethod
    def min_chunk_positive(cls, v: int | None):
        if v is not None and v <= 0:
            raise ValueError("min_chunk must be positive when provided")
        return v

    @field_validator("max_duration_chunk")
    @classmethod
    def max_duration_chunk_positive(cls, v: int | None):
        if v is not None and v <= 0:
            raise ValueError("max_duration_chunk must be positive when provided")
        return v

    @field_validator("schedule_name")
    @classmethod
    def clean_schedule_name(cls, v: str | None):
        if v is None:
            return v
        v = v.strip()
        if not v:
            raise ValueError("schedule_name cannot be blank")
        return v


class TaskOut(Schema):
    """Task in API responses (create + list)."""

    id: int
    user_id: int
    title: str
    description: str
    duration: int
    priority: int
    deadline: datetime | None
    is_hard_deadline: bool
    status: str
    start_date: datetime | None
    min_chunk: int | None
    max_duration_chunk: int | None
    schedule_id: int | None = None
    schedule_name: str | None = None
