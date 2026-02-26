from datetime import datetime
from typing import Optional

from ninja import Schema
from pydantic import field_validator


class StateIn(Schema):
    state: str

    @field_validator("state")
    def validate_state(cls, v):
        if not v:
            raise ValueError("State is required")
        return v


class StateOut(Schema):
    ok: bool
    state: str
    error: Optional[str] = None


class OAuthCallbackIn(Schema):
    code: str
    state: str

    @field_validator("code", "state")
    @classmethod
    def not_empty(cls, v: str):
        if not v.strip():
            raise ValueError("Must not be empty")
        return v


class OAuthCallbackOut(Schema):
    jwt_token: str
    expiry_date: datetime
    ok: bool


class OAuthCallbackError(Schema):
    ok: bool
    error: str
