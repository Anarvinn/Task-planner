from __future__ import annotations
from exceptions import ValidationError, StorageError, TaskNotFoundError, DuplicateTaskIdError, DependencyError
from models.enum import PriorityType, StatusType
from models.dependency import DependencyChecker
from storage.json_storage import JsonStorage
from models.task import Task
from copy import deepcopy
from typing import Any


class Manager:
    def __init__(self, storage: JsonStorage) -> None:
        self._storage = storage
        self._dependency = DependencyChecker(self)
        self._tasks: dict[str, Task] = {}

        self._load_data()

    def _load_data(self) -> None:
        raw_tasks = self._storage.load()
        try:
            for id, item in raw_tasks.items():
                task = Task(
                    id=item['id'],
                    title=item['title'],
                    priority=PriorityType(item['priority']),
                    status=StatusType(item['status']),
                    dependency=item['dependency']
                )
                self._tasks[id] = task
        except (KeyError, TypeError, ValueError, ValidationError) as e:
            raise StorageError(f"Invalid task data in storage: {e}") from e

    def get_task(self, id: str) -> Task:

        try:
            return self._tasks[id]
        except KeyError:
            raise TaskNotFoundError(f"Task {id} was not found") from None

    def get_all_tasks(self) -> list[Task]:
        return deepcopy(list(self._tasks.values()))

    def add_task(self, title: str, priority: PriorityType) -> Task:

        def operation() -> None:
            task = Task(title, priority)

            if task.id in self._tasks:
                raise DuplicateTaskIdError(
                    f"ID {task.id} already exists"
                )

            self._tasks[task.id] = deepcopy(task)
            return deepcopy(task)

        return self.execute_and_save(operation)

    def edit_task(
        self,
        id: str,
        *,
        new_title: str | None = None,
        new_priority: str | None = None
    ) -> Task:

        def operation() -> Task:
            task = self.get_task(id)

            updated = deepcopy(task)
            updated.update(
                title=new_title,
                priority=new_priority
            )
            if updated.id != task.id and updated.id is self._tasks:
                raise DuplicateTaskIdError(
                    f"Id {updated.id} already exists"
                )
            if updated.id != task.id:
                del self._tasks[task.id]

            self._tasks[updated.id] = updated

            return deepcopy(updated)

        return self.execute_and_save(operation)

    def delete_task(self, id_task: str) -> list[dict[str, Task]]:

        def operation() -> list[dict[str, Task]]:
            if self._dependency.validate_task_deletion(id_task):
                self.get_task(id_task)

                del self._tasks[id_task]
                return deepcopy(self._tasks)

        return self.execute_and_save(operation)

    def add_dependency(self, id_task: str, id_dependency: str) -> Task:

        def operation() -> Task:
            if self._dependency.validate_dependency(id_task, id_dependency,):
                task = self.get_task(id_task)
                task.add_dependency(id_dependency)
                return deepcopy(task)

        return self.execute_and_save(operation)

    def remove_dependency(self, id_task: str, id_dependency: str) -> Task:

        def operation() -> Task:
            task = self.get_task(id_task)
            if id_dependency in task.dependency:
                task.remove_dependency(id_dependency)
            else:
                raise DependencyError(
                    "The task does not have such a dependency")
            return deepcopy(task)

        self.execute_and_save(operation)

    def advance_task_status(self, id_task: str) -> Task:

        def operation() -> Task:
            task = self.get_task(id_task)
            if not self._dependency.are_dependencies_completed(task):
                raise DependencyError(
                    "You cannot start a task until all dependencies are completed")
            if task.status == "Done":
                raise ValidationError(
                    "The task has already been completed")
            task.status = (StatusType.IN_WORK, StatusType.DONE)[
                task.status == "In work"]
            return deepcopy(task)

        return self.execute_and_save(operation)

    def show_completed_tasks(self) -> list[Task]:
        ready_tasks = []
        for task in self.get_all_tasks():
            if task.status == "Done":
                ready_tasks.append(task)

        return self.sort_tasks(ready_tasks)

    def show_tasks_ready_to_start(self) -> list[Task]:
        ready_tasks = set()
        for task in self.get_all_tasks():
            if self._dependency.are_dependencies_completed(task) and task.status != "Done":
                ready_tasks.add(task)
        return self.sort_tasks(list(ready_tasks))

    def show_all_tasks(self) -> list[Task]:
        return self.sort_tasks(self.get_all_tasks())

    def execute_and_save(self, operation) -> Any:
        previous_tasks = deepcopy(self._tasks)

        try:
            result = operation()
            self._storage.save(self._tasks)
            return result
        except Exception:
            self._tasks = previous_tasks
            raise

    def search_tasks(self, query: str) -> list[Task]:
        query = query.casefold()
        return deepcopy([
            task
            for task in self._tasks.values()
            if query in task.title.casefold()
            or query in task.id.casefold()
        ])

    def sort_tasks(self, tasks: list[Task]) -> list[Task]:
        return sorted(tasks, key=lambda t: (t.priority, t.id), reverse=True)
