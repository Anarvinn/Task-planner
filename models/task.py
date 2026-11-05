from dataclasses import dataclass, field
from validation_helpers import validate_title, validate_priority, validate_status
from enum import StrEnum
import uuid


class PriorityType(StrEnum):
    HIGHT = 'hight'
    MEDIUM = 'medium'
    LOW = 'low'


class StatusType(StrEnum):
    NEW = 'new'
    IN_WORK = 'in_work'
    DONE = 'done'


@dataclass
class Task:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    priority: PriorityType
    status: StatusType = field(default=StatusType.NEW)
    dependence: list = field(default_factory=list)

    def __post_init__(self) -> None:
        self.title = validate_title(self.title, "Title")

    def update(
            self,
            *,
            new_title: str | None = None,
            new_priority: str | None = None,
            new_status: str | None = None
    ) -> None:
        if new_title is not None:
            self.title = validate_title(new_title, "Title")

        if new_priority is not None:
            self.priority = validate_priority(new_priority, "Priority")

        if new_status is not None:
            self.status = validate_status(new_status, "Status")
