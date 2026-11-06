from __future__ import annotations
from enum import StrEnum
from functools import total_ordering


@total_ordering
class PriorityType(StrEnum):
    HIGH = 'High'
    MEDIUM = 'Medium'
    LOW = 'Low'

    @property
    def weight(self) -> int:
        mapping = {
            'High': 3,
            'Medium': 2,
            'Low': 1
        }
        return mapping[self.value]

    def __lt__(self, other: PriorityType) -> bool:
        if not isinstance(other, PriorityType):
            return NotImplemented
        return (self.weight < other.weight)


class StatusType(StrEnum):
    NEW = 'New'
    IN_WORK = 'In work'
    DONE = 'Done'
