from __future__ import annotations
from exceptions import DependencyError
from .task import Task


class DependencyChecker:
    def __init__(self, manager) -> None:
        self._manager = manager

    def validate_distinct_task_ids(self, id_task: str, dependency_id: str) -> bool:
        if id_task == dependency_id:
            raise DependencyError("You can't link a task to yourself")
        return True

    def validate_dependency(self, id_task: str, dependency_id: str,) -> bool:
        self.validate_distinct_task_ids(id_task, dependency_id)

        if dependency_id in self._manager.get_task(id_task).dependency:
            raise DependencyError("This dependency already exists")

        if self._manager.get_task(id_task).status == "Done":
            raise DependencyError(
                "Cannot add a dependency to a completed task")

        dependency_task = self._manager.get_task(dependency_id)
        if dependency_task.dependency:
            for dep in dependency_task.dependency:
                if id_task == dep:
                    raise DependencyError(
                        "Circular dependencies are not allowed")
                self.validate_dependency(id_task, dep)
        return True

    def validate_task_deletion(self, id_task: str) -> bool:
        for task in self._manager.get_all_tasks():
            if id_task in task.dependency:
                raise DependencyError(
                    "You cannot delete a task that others depend on")
        return True

    def are_dependencies_completed(self, task: Task) -> bool:
        for dependency in task.dependency:
            dependency = self._manager._tasks[dependency]
            if dependency.status != "Done":
                return False
        return True
