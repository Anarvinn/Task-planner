from __future__ import annotations
from exceptions import ValidationError, StorageError, TaskNotFoundError, DuplicateIdError, DependenceError
from models.enum import PriorityType, StatusType
from models.dependence import CheckDependence
from storage.json_storage import JsonStorage
from models.task import Task
from copy import deepcopy
from typing import Any


class Manager:
    def __init__(self, storage: JsonStorage) -> None:
        self._storage = storage
        self._dependence = CheckDependence(self)
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
                    dependence=item['dependence']
                )
                self._tasks[id] = task
        except (KeyError, TypeError, ValueError, ValidationError) as e:
            raise StorageError(f"Invalid manager data: {e}") from e

    def get_task(self, id: str) -> Task:

        try:
            return self._tasks[id]
        except KeyError:
            raise TaskNotFoundError(f"Task {id} was not found") from None

    def get_all_task(self) -> list[Task]:
        return deepcopy(list(self._tasks.values()))

    def add_task(self, task: Task) -> Task:

        def operation() -> None:
            if task.id in self._tasks:
                raise DuplicateIdError(
                    f"ID {task.id} already exists"
                )

            self._tasks[task.id] = deepcopy(task)

        self.record(operation)

    def edit_task(
        self,
        id: str,
        *,
        new_title: str | None = None,
        new_priority: str | None = None,
        new_status: str | None = None
    ) -> None:

        def operation() -> Task:
            task = self.get_task(id)

            updated = deepcopy(task)
            updated.update(
                title=new_title,
                priority=new_priority,
                status=new_status
            )
            if updated.id != task.id and updated.id is self._tasks:
                raise DuplicateIdError(
                    f"Id {updated.id} already exists"
                )
            if updated.id != task.id:
                del self._tasks[task.id]

            self._tasks[updated.id] = updated

            return deepcopy(updated)

        return self.record(operation)

    def del_task(self, task: Task) -> None:

        def operation() -> list[dict[str, Task]]:
            if self._dependence.check_del_task(task.id):

                del self._tasks[task.id]
                return deepcopy(self._tasks)

        return self.record(operation)

    def add_dependence(self, id_task: str, id_dependence: str) -> None:

        def operation() -> Task:
            if self._dependence.check_add_dependence(id_task, id_dependence,):
                task = self.get_task(id_task)
                task.add_dependence(id_dependence)
                return deepcopy(task)

        return self.record(operation)

    def del_dependence(self, id_task: str, id_dependence: str) -> None:

        def operation() -> Task:
            task = self.get_task(id_task)
            if id_dependence in task.dependence:
                task.del_dependence(id_dependence)
            else:
                raise DependenceError(
                    "The task does not have such a dependency")
            return deepcopy(task)

        self.record(operation)

    def next_stage(self, id_task: str) -> None:

        def operation() -> Task:
            task = self.get_task(id_task)
            if self._dependence.readiness_check(task):
                if task.status == "Done":
                    raise DependenceError(
                        "The task has already been completed")
                task.status = (StatusType.IN_WORK, StatusType.DONE)[
                    task.status == "In work"]
                return deepcopy(task)

        self.record(operation)

    def show_ready_tasks(self) -> list[Task]:
        ready_tasks = []
        for task in self.get_all_task():
            if task.status == "Done":
                ready_tasks.append(task)

        return self.sorted_tasks(ready_tasks)

    def show_ready_to_start_tasks(self) -> list[Task]:
        ready_tasks = set()
        for task in self.get_all_task():
            if self._dependence.readiness_check(task) and task.status != "Done":
                ready_tasks.add(task)
        return self.sorted_tasks(list(ready_tasks))

    def show_all_tasks(self) -> list[Task]:
        return self.sorted_tasks(self.get_all_task)

    def record(self, operation) -> Any:
        previous_tasks = deepcopy(self._tasks)

        try:
            result = operation()
            self._storage.save(self._tasks)
            return result
        except Exception:
            self._tasks = previous_tasks
            raise

    def search_task(self, query: str) -> list[Task]:
        query = query.casefold()
        return deepcopy([
            task
            for task in self._tasks.values()
            if query in task.title.casefold()
            or query in task.id.casefold()
        ])

    def sorted_tasks(self, tasks: list[Task]) -> list[Task]:
        return sorted(tasks, key=lambda t: (t.priority, t.id), reverse=True)
