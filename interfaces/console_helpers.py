from exceptions import ValidationError
from models.enum import PriorityType
from models.task import Task


def read_text(pattern: str) -> str:
    while True:
        text = input(pattern).strip()

        if text:
            return text

        print("Input cannot be empty")


def get_priority() -> PriorityType:
    options = {
        '1': PriorityType.LOW,
        '2': PriorityType.MEDIUM,
        '3': PriorityType.HIGH
    }

    print(
        "\n1. Low\n"
        "2. Medium\n"
        "3. High\n")

    choice = input("Select priority: ").strip()

    if choice not in options:
        raise ValidationError("Invalid priority option")

    return options[choice]


def print_tasks(tasks: list[Task]):
    if not tasks:
        print("No task found")
        return

    print(
        f"\n{'TITLE':<20}"
        f"{'PRIORITY':<10}"
        f"{'STATUS':<10}"
        f"{'DEPENDENCE':<12}"
        f"{'ID':>10}"
    )
    print('-' * 91)

    for task in tasks:
        print(
            f"{task.title:<20}"
            f"{task.priority:<10}"
            f"{task.status:<10}"
            f"{len(task.dependence):<15}"
            f"{task.id:>10}"
        )
