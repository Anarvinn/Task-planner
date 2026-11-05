from services.manager import Manager
from exceptions import ManagerError
from models.task import Task
from console_helpers import read_text, print_tasks, get_priority, get_status


class ConsoleMenu:
    def __init__(self, manager: Manager) -> None:
        self.manager = manager

    def run(self) -> None:

        actions = {
            '1': self.add_task,
            '2': self.edit_task,
            '3': self.del_task,
            '4': self.add_dependence,
            '5': self.del_dependence,
            '6': self.show_ready_tasks,
            '7': self.show_all_tasks
        }

        while True:
            print(
                "\n========== TASK MANAGER ==========\n"
                "1. Add task\n"
                "2. Edit task\n"
                "3. Delate task"
                "4. Add dependencies\n"
                "5. Delate dependencies\n"
                "6. Show ready task\n"
                "7. Show all task\n"
                "0. Exit\n"
                "=================================="
            )

            choice = input("Select action: ").strip()

            if choice == '0':
                print("Program closed")
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

        title = read_text("Title: ")
        priority = get_priority()

        task = Task(
            title=title,
            priority=priority
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

    def del_task(self) -> None:
        id_task = read_text("Task ID: ")
        task = self.manager.get_task(id_task)
        choice = read_text("Are you sure you want to delete the task? Y/N: ")
        if choice == 'Y':
            self.manager.del_task(task)
            print("Task successfully deleted")
        elif choice == 'N':
            return
        else:
            print("Invalid choice")

    def add_dependence(self) -> None:
        id_task = read_text("Task ID: ")
        self.manager.get_task(id_task)

        print("\nEnter the ID of the task you want to link")
        id_dependence = read_text("Dependence ID: ")

        self.manager.add_dependence(id_task, id_dependence)
        print("Dependence successfully added")

    def del_dependence(self) -> None:
        id_task = read_text("Task ID: ")
        self.manager.get_task(id_task)

        print("\nEnter the ID of the task you want to delete")
        id_dependence = read_text("Dependence ID: ")

        self.manager.del_dependence(id_task, id_dependence)
        print("Dependence successfully deleted")

    def show_ready_tasks(self) -> None:
        tasks = self.manager.show_ready_tasks()

        print_tasks(tasks)

    def show_all_tasks(self) -> None:
        tasks = self.manager.show_all_tasks()

        print_tasks(tasks)
