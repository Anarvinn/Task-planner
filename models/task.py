from __future__ import annotations
from dataclasses import dataclass, field
from models.validation_helpers import validate_text, validate_priority, validate_status
from models.enum import PriorityType, StatusType
import uuid


@dataclass
class Task:
    title: str
    priority: PriorityType
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: StatusType = field(default=StatusType.NEW)
    dependence: list = field(default_factory=list)

    def __post_init__(self) -> None:
        self.title = validate_text(self.title, "Title")
        self.priority = validate_priority(self.priority, "Priority")

    def update(
            self,
            *,
            title: str | None = None,
            priority: str | None = None,
            status: str | None = None
    ) -> None:
        if title is not None:
            self.title = validate_text(title, "Title")

        if priority is not None:
            self.priority = validate_priority(priority, "Priority")

        if status is not None:
            self.status = validate_status(status, "Status")

    def add_dependence(self, id_new_dependence: str) -> None:
        self.dependence.append(id_new_dependence)

    def del_dependence(self, id_del_dependence: str) -> None:
        self.dependence.remove(id_del_dependence)
