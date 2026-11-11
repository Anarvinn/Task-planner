from models.enum import PriorityType, StatusType
from exceptions import ValidationError
from models.task import Task
import pytest


def test_validation_error():
    with pytest.raises(ValidationError):
        Task('', 'Low')

    with pytest.raises(ValidationError):
        Task([], 'Low')

    with pytest.raises(ValidationError):
        Task('Test', '')

    with pytest.raises(ValidationError):
        Task('Test', 'Test')


def test_correct_task():
    task = Task('Correct title', 'High')

    assert task.title == 'Correct title'
    assert task.priority == PriorityType.HIGH
    assert task.status == StatusType.NEW
    assert task.dependence == []


def test_validate_update_task(manager, sample_task):
    task = sample_task
    old_title = task.title
    old_priority = task.priority

    with pytest.raises(ValidationError):
        manager.edit_task(id=task.id, new_title='')
    assert task.title == old_title

    with pytest.raises(ValidationError):
        manager.edit_task(id=task.id, new_priority='')
    assert task.priority == old_priority


def test_correct_update_task(manager, sample_task):
    task = sample_task
    id = task.id
    manager.edit_task(id=id, new_title='New title')
    manager.edit_task(id=id, new_priority='High')
    manager.next_stage(id_task=id)
    task = manager.get_task(id)

    assert task.id == id
    assert task.title == 'New title'
    assert task.priority == PriorityType.HIGH
    assert task.status == StatusType.IN_WORK
