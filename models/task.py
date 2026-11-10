from __future__ import annotations
from models.validation_helpers import validate_text, validate_priority, validate_status
from models.enum import PriorityType, StatusType
from dataclasses import dataclass, field
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
            priority: str | None = None
    ) -> None:

        if title is not None:
            self.title = validate_text(title, "Title")

        if priority is not None:
            self.priority = validate_priority(priority, "Priority")

    def add_dependence(self, id_new_dependence: str) -> None:
        self.dependence.append(id_new_dependence)

    def del_dependence(self, id_del_dependence: str) -> None:
        self.dependence.remove(id_del_dependence)

    def __hash__(self):
        return hash(self.id)
