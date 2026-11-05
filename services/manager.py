from models.dependence import CheckDependence
from models.task import Task
from storage.json_storage import JsonStorage
from exceptions import *
from copy import deepcopy


class Manager:
    def __init__(self, storage: JsonStorage) -> None:
        self._storage = storage
        self.dependence = CheckDependence()
        self._tasks = dict[str, Task] = {}

        self._load_data()

    def load_data(self) -> None:
        raw_tasks = self._storage.load()
        try:
            for id, item in raw_tasks.items():
                task = Task(
                    id=item['id'],
                    title=item['title'],
                    priority=item['priority'],
                    status=item['status'],
                    dependence=item['dependence']
                )
                self._tasks[id] = task
        except (KeyError, TypeError, ValueError, ValidationError) as e:
            raise StorageError(f"Invalid manager data: {e}") from e

    def get_task(self, id: str) -> Task:

        try:
            return deepcopy(self._tasks.get(id))
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
                id=id,
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
            if self.dependence.check_del_task(task.id):
                tasks = deepcopy(self._tasks)
                del tasks[task.id]
                return deepcopy(tasks)

        return self.record(operation)

    def add_dependence(self, id_task: str, id_dependence: str) -> None:

        def operation() -> Task:
            if self.dependence.check_add_dependence(id_task, id_dependence):
                task = self.get_task(id_task)
                task.add_dependence(id_dependence)
                return deepcopy(task)

        return self.record(operation)

    def del_dependence(self, id_task: str, id_dependence: str) -> None:

        def operation() -> Task:
            task = self.get_task(id_task)
            if id_dependence in task.add_dependence:
                task.del_dependence(id_dependence)
            else:
                raise DependenceError(
                    "The task does not have such a dependency")
            return deepcopy(task)

        self.record(operation)

    def show_ready_tasks(self) -> list[Task]:
        ready_tasks = []
        for task in self.get_all_task():
            if task.status == 'done':
                ready_tasks.append(task)

        result = sorted(result, key=lambda t: (t.priority, t.id))
        return result

    def show_all_tasks(self) -> list[Task]:
        result = self.get_all_tasks()
        result = sorted(result, key=lambda t: (t.priority, t.id))
        return result

    def record(self, operation):
        previous_tasks = deepcopy(self._tasks)

        try:
            result = operation()
            self._storage.save(self._tasks)
            return result
        except Exception:
            self._tasks = previous_tasks
            raise
