from exceptions import ValidationError
from models.task import PriorityType, StatusType


def validate_text(text: str, field: str) -> str:
    if not isinstance(text, str) or not text.strip():
        raise ValidationError(f"{field} cannot be empty")
    return text


def validate_priority(priority: str, field: str) -> PriorityType:
    priority = validate_text(priority, field)
    try:
        priority = PriorityType(priority)
    except ValueError:
        raise ValidationError("There is no such priority")
    return priority


def validate_status(status: str, field: str) -> StatusType:
    status = validate_text(status, field)
    try:
        status = StatusType(status)
    except ValueError:
        raise ValidationError("There is no such status")
