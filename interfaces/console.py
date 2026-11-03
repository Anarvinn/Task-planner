from services.manager import Manager
from exceptions import ManagerError
from models.task import Task
from console_helpers import read_text


class ConsoleMenu:
    def __init__(self, manager: Manager) -> None:
        self.manager = manager

    def run(self) -> None:

        actions = {
            '1': self.add_task,
            '2': self.edit_task,
            '3': self.add_dependence,
            '4': self.del_dependencies,
            '5': self.show_ready_task,
            '6': self.show_all_task
        }

        while True:
            print(
                "\n========== TASK MANAGER ==========\n"
                "1. Add task\n"
                "2. Edit task\n"
                "3. Add dependencies\n"
                "4. Delate dependencies\n"
                "5. Show ready task\n"
                "6. Show all task\n"
                "0. Exit\n"
                "=================================="
            )

            choice = input("Select action: ").strip()

            if choice == '0':
                print("program closed")
                break

            actions = actions.get(choice)

            if actions is None:
                print("Unknown menu option")
                continue

            try:
                actions()
            except ManagerError as e:
                print(f"\nManager error: {e}")
            except (ValueError, TypeError) as e:
                print(f"\nInput error: {e}")

    def add_task(self) -> None:

        task = Task(
            title=read_text("Title: "),
            priority=read_text("Priotity: "),
        )

        self.manager.add_task(task)
        print("Task successfully added")

    def edit_task(self) -> None:
        id = read_text("Task ID: ")
        task = self.manager.get_task(id)
        print("\nLeave the field empty to keep its current value")

        new_title = input(
            f"Title [{task.title}]: "
        ).strip()

        new_priority = input(
            f"Priority [{task.priority}]: "
        ).strip()

        new_status = input(
            f"Status [{task.status}]: "
        ).strip()

        self.manager.edit_task(
            id,
            new_title=new_title or None,
            new_priority=new_priority or None,
            new_status=new_status or None
        )

        print("Task successfully updated")

    def add_dependence(self) -> None:
        id_task = read_text("Task ID: ")
        task = self.manager.get_task(id_task)

        print("\nEnter the ID of the task you want to link")
        id_dependence = read_text("Dependence ID: ")

        self.manager.add_dependence(task, id_dependence)
        print("Dependence successfully added")

    def del_dependence(self) -> None:
        id_task = read_text("Task ID: ")
        task = self.manager.get_task(id_task)

        print("\nEnter the ID of the task you want to delete")
        id_dependence = read_text("Dependence ID: ")

        self.manager.del_dependence(task, id_dependence)
        print("Dependence successfully deleted")
