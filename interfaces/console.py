from interfaces.console_helpers import read_text, print_tasks, get_priority
from services.manager import Manager
from exceptions import ManagerError
from models.task import Task


class ConsoleMenu:
    def __init__(self, manager: Manager) -> None:
        self.manager = manager

    def run(self) -> None:

        while True:
            actions = {
                '1': self.add_task,
                '2': self.edit_task,
                '3': self.delete_task,
                '4': self.add_dependency,
                '5': self.remove_dependency,
                '6': self.advance_task_status,
                '7': self.show_tasks_ready_to_start,
                '8': self.show_completed_tasks,
                '9': self.show_all_tasks,
                '10': self.search_tasks,
            }

            print(
                "\n========== TASK MANAGER ==========\n"
                "1. Add task\n"
                "2. Edit task\n"
                "3. Delete task\n"
                "4. Add dependency\n"
                "5. Remove dependency\n"
                "6. Advance task status\n"
                "7. Show tasks ready to start\n"
                "8. Show completed tasks\n"
                "9. Show all task\n"
                "10. Search tasks\n"
                "0. Exit\n"
                "=================================="
            )

            choice = input("Select action: ").strip()

            if choice == '0':
                print("Application closed")
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

        self.manager.add_task(title, priority)
        print("Task added successfully")

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

        self.manager.edit_task(
            id,
            new_title=new_title or None,
            new_priority=new_priority or None
        )

        print("Task updated successfully")

    def delete_task(self) -> None:
        id_task = read_text("Task ID: ")
        self.manager.get_task(id_task)
        choice = read_text(
            "Are you sure you want to delete the task? Y/N: ").upper()
        if choice == 'Y':
            self.manager.delete_task(id_task)
            print("Task deleted successfully")
        elif choice == 'N':
            return
        else:
            print("Invalid choice")

    def add_dependency(self) -> None:
        id_task = read_text("Task ID: ")
        self.manager.get_task(id_task)

        print("\nEnter the ID of the task you want to link\n")
        id_dependency = read_text("Dependency ID: ")

        self.manager.add_dependency(id_task, id_dependency)
        print("Dependency added successfully")

    def remove_dependency(self) -> None:
        id_task = read_text("Task ID: ")
        self.manager.get_task(id_task)

        print("\nEnter the ID of the task you want to delete")
        id_dependency = read_text("Dependency ID: ")

        self.manager.remove_dependency(id_task, id_dependency)
        print("Dependency removed successfully")

    def advance_task_status(self) -> None:
        id_task = read_text("Task ID: ")
        self.manager.advance_task_status(id_task)
        print("Task status updated successfully")

    def show_tasks_ready_to_start(self) -> None:
        tasks = self.manager.show_tasks_ready_to_start()
        print_tasks(tasks)

    def show_completed_tasks(self) -> None:
        tasks = self.manager.show_completed_tasks()

        print_tasks(tasks)

    def show_all_tasks(self) -> None:
        tasks = self.manager.show_all_tasks()

        print_tasks(tasks)

    def search_tasks(self) -> None:
        query = read_text("Search: ")
        tasks = self.manager.search_tasks(query)

        print_tasks(tasks)
