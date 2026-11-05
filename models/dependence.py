from models.task import Task
from services.manager import Manager
from exceptions import DependenceError


class CheckDependence:
    def __init__(self):
        self.manager = Manager()

    def different_id(self, id_task: str, id_new_dependence: str) -> bool:
        if id_task == id_new_dependence:
            raise DependenceError("You can't link a task to yourself.")
        return True

    def check_add_dependence(self, id_task: str, id_new_dependence: str,) -> bool:

        task_dependence = self.manager.get_task(id_new_dependence)
        if task_dependence.dependence:
            for dep in task_dependence.dependence:
                if self.different_id(id_task, dep):
                    self.check_add_dependence(id_task, dep)
        return True

    def check_del_task(self, id_task: str) -> bool:
        for task in self.manager.get_all_task():
            if id_task in task.dependence:
                raise DependenceError(
                    "You cannot delete a task that others depend on")
        return True
