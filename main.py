# from __future__ import annotations
from storage.json_storage import JsonStorage
from interfaces.console import ConsoleMenu
from services.manager import Manager
from exceptions import StorageError


def main() -> None:

    storage = JsonStorage('tasks.json')

    try:
        manager = Manager(storage)

        menu = ConsoleMenu(manager)
        menu.run()
    except (StorageError, OSError) as e:
        print(f"Application startup error: {e}")


if __name__ == "__main__":
    main()
