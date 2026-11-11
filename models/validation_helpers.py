from __future__ import annotations
from models.enum import PriorityType, StatusType
from exceptions import ValidationError


def validate_text(text: str, field: str) -> str:
    if not isinstance(text, str) or not text.strip():
        raise ValidationError(f"{field} cannot be empty")
    return text.capitalize()


def validate_priority(priority: str, field: str) -> PriorityType:
    priority = validate_text(priority, field)
    try:
        priority = PriorityType(priority)
    except ValueError:
        raise ValidationError("Invalid priority value")
    return priority


def validate_status(status: str, field: str) -> StatusType:
    status = validate_text(status, field)
    try:
        status = StatusType(status)
    except ValueError:
        raise ValidationError("Invalid status value")
    return status
