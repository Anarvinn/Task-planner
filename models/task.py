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
    dependency: list = field(default_factory=list)

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

    def add_dependency(self, dependency_id: str) -> None:
        self.dependency.append(dependency_id)

    def remove_dependency(self, id_remove_dependency: str) -> None:
        self.dependency.remove(id_remove_dependency)

    def __hash__(self):
        return hash(self.id)
