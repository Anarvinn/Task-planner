from __future__ import annotations
from exceptions import DependenceError
from .task import Task


class CheckDependence:
    def __init__(self, manager) -> None:
        self._manager = manager

    def different_id(self, id_task: str, id_new_dependence: str) -> bool:
        if id_task == id_new_dependence:
            raise DependenceError("You can't link a task to yourself.")
        return True

    def check_add_dependence(self, id_task: str, id_new_dependence: str,) -> bool:
        self.different_id(id_task, id_new_dependence)

        if id_new_dependence in self._manager.get_task(id_task).dependence:
            raise DependenceError("You have already linked this task.")

        task_dependence = self._manager.get_task(id_new_dependence)
        if task_dependence.dependence:
            for dep in task_dependence.dependence:
                if id_task == dep:
                    raise DependenceError(
                        "You can't create a looped connection.")
                self.check_add_dependence(id_task, dep)
        return True

    def check_del_task(self, id_task: str) -> bool:
        for task in self._manager.get_all_task():
            if id_task in task.dependence:
                raise DependenceError(
                    "You cannot delete a task that others depend on")
        return True

    def readiness_check(self, task: Task) -> bool:
        for dependence in task.dependence:
            dependence = self._manager._tasks[dependence]
            if dependence.status != "Done":
                return False
        return True
