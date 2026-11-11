from models.enum import PriorityType, StatusType


def test_priority_ordering() -> None:

    assert PriorityType.HIGH > PriorityType.MEDIUM
    assert PriorityType.MEDIUM > PriorityType.LOW
    assert PriorityType.HIGH > PriorityType.LOW


def test_status_values() -> None:
    assert StatusType.DONE == "Done"
    assert StatusType.IN_WORK == "In work"
    assert StatusType.NEW == "New"
