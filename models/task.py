from __future__ import annotations
from dataclasses import dataclass, field
from models.validation_helpers import validate_text, validate_priority, validate_status
from functools import total_ordering
from enum import StrEnum
import uuid


@total_ordering
class PriorityType(StrEnum):
    HIGHT = 'hight'
    MEDIUM = 'medium'
    LOW = 'low'

    @property
    def weight(self) -> int:
        mapping = {
            'hight': 3,
            'medium': 2,
            'low': 1
        }
        return mapping[self.value]

    def __lt__(self, other: PriorityType) -> bool:
        if not isinstance(self, other):
            return NotImplemented
        return (self.weight < other.weight)


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
        self.title = validate_text(self.title, "Title")

    def update(
            self,
            *,
            new_title: str | None = None,
            new_priority: str | None = None,
            new_status: str | None = None
    ) -> None:
        if new_title is not None:
            self.title = validate_text(new_title, "Title")

        if new_priority is not None:
            self.priority = validate_priority(new_priority, "Priority")

        if new_status is not None:
            self.status = validate_status(new_status, "Status")

    def add_dependence(self, id_new_dependence: str) -> None:
        self.dependence.append(id_new_dependence)

    def del_dependence(self, id_del_dependence: str) -> None:
        self.dependence.remove(id_del_dependence)
