from exceptions import DependencyError, TaskNotFoundError, ValidationError
from storage.json_storage import JsonStorage
from services.manager import Manager
from models.enum import StatusType
import pytest


def test_manager_restores_tasks_from_storage(manager):
    task1 = manager.add_task('First', 'High')
    task2 = manager.add_task('Second', 'Medium')
    task3 = manager.add_task('Last', 'Low')
    manager._storage.save(manager._tasks)

    storage = JsonStorage(manager._storage.filepath)
    restored_manager = Manager(storage)
    restored_manager._load_data()
    tasks = restored_manager.show_all_tasks()
    restored_tasks1 = tasks[0]
    restored_tasks2 = tasks[1]
    restored_tasks3 = tasks[2]

    assert len(tasks) == 3
    assert task1 == restored_tasks1
    assert task2 == restored_tasks2
    assert task3 == restored_tasks3


def test_tasks_are_sorted_by_priority(manager):
    manager.add_task('First', 'High')
    manager.add_task('Second', 'Medium')
    manager.add_task('Last', 'Low')

    sort_tasks = manager.show_all_tasks()
    assert len(sort_tasks) == 3
    assert sort_tasks[0].title == 'First'
    assert sort_tasks[1].title == 'Second'
    assert sort_tasks[2].title == 'Last'


def test_show_completed_tasks_returns_only_completed_tasks(manager, sample_task):
    id = sample_task.id
    manager.add_task('Second task', 'High')
    manager.advance_task_status(id)
    manager.advance_task_status(id)
    sort_tasks = manager.show_completed_tasks()

    assert len(sort_tasks) == 1
    assert sort_tasks[0].status == StatusType.DONE
    assert sort_tasks[0].title == 'Test task'


def test_show_tasks_ready_to_start_excludes_blocked_tasks(manager, sample_task):

    task1 = sample_task
    task2 = manager.add_task('Test 2', 'Medium')
    task3 = manager.add_task('Test 3', 'High')
    manager.advance_task_status(task1.id)
    manager.advance_task_status(task1.id)
    manager.add_dependency(task2.id, task3.id)

    sort_tasks = manager.show_tasks_ready_to_start()
    assert len(sort_tasks) == 1
    assert sort_tasks[0].title == 'Test 3'


def test_manager_validates_dependencies(manager, sample_task):
    task1 = sample_task
    task2 = manager.add_task('Test task 2', 'Medium')

    task1 = manager.add_dependency(task1.id, task2.id)

    assert len(task1.dependency) == 1
    with pytest.raises(DependencyError):
        manager.add_dependency(task2.id, task1.id)
    assert len(task2.dependency) == 0

    with pytest.raises(DependencyError):
        manager.add_dependency(task1.id, task1.id)
    assert len(task1.dependency) == 1

    with pytest.raises(DependencyError):
        manager.advance_task_status(task1.id)
    assert task1.status == StatusType.NEW

    with pytest.raises(DependencyError):
        manager.delete_task(task2.id)
    assert len(manager.get_all_tasks()) == 2

    with pytest.raises(TaskNotFoundError):
        manager.add_dependency(task1.id, '123')

    assert len(task1.dependency) == 1
    assert task2.id in task1.dependency


def test_manager_deletes_task(manager, sample_task):
    id = sample_task.id
    old_list_tasks = manager.get_all_tasks()

    new_list_tasks = manager.delete_task(id)

    assert len(old_list_tasks) == 1
    assert len(new_list_tasks) == 0
    with pytest.raises(TaskNotFoundError):
        manager.delete_task('123')


def test_unknown_task_id_raises_error(manager, sample_task):
    old_list = manager.get_all_tasks()
    with pytest.raises(TaskNotFoundError):
        manager.edit_task('123', new_title='New title', new_priority='Medium')

    with pytest.raises(TaskNotFoundError):
        manager.advance_task_status('123')

    with pytest.raises(TaskNotFoundError):
        manager.get_task('123')
    new_list = manager.get_all_tasks()

    assert len(old_list) == 1
    assert len(old_list) == len(new_list)
    assert old_list == new_list


def test_manager_handles_empty_storage(tmp_path):
    storage = JsonStorage(tmp_path / "test_tasks.json")
    manager = Manager(storage)

    all_tasks = manager.get_all_tasks()
    ready_to_start_tasks = manager.show_tasks_ready_to_start()
    completed_tasks = manager.show_completed_tasks()
    assert len(all_tasks) == 0
    assert len(ready_to_start_tasks) == 0
    assert len(completed_tasks) == 0


def test_dependencies_are_restored_from_storage(manager, sample_task):
    task1 = sample_task
    task2 = manager.add_task('Task 2', 'High')

    manager.add_dependency(task1.id, task2.id)
    manager._storage.save(manager._tasks)

    storage = JsonStorage(manager._storage.filepath)
    restored_manager = Manager(storage)
    restored_task1 = restored_manager.get_task(task1.id)
    restored_task2 = restored_manager.get_task(task2.id)

    assert restored_task2.id in restored_task1.dependency


def test_task_status_lifecycle(manager, sample_task):
    task = sample_task
    assert task.status == StatusType.NEW

    task = manager.advance_task_status(task.id)
    assert task.status == StatusType.IN_WORK

    task = manager.advance_task_status(task.id)
    assert task.status == StatusType.DONE

    with pytest.raises(ValidationError):
        assert manager.advance_task_status(task.id)
