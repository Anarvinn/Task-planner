from models.task import PriorityType, StatusType


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
        '3': PriorityType.HIGHT
    }

    print(
        "\n1. Low\n"
        "2. Medium\n"
        "3. Hight\n")

    choice = input("Select priority").strip()

    if choice not in options:
        print("Invalid priority option")
        return

    return options[choice]


def get_status() -> StatusType:
    options = {
        '1': StatusType.NEW,
        '2': StatusType.IN_WORK,
        '3': StatusType.DONE
    }

    print(
        "\n1. New\n"
        "2. In work\n"
        "3. Done\n")

    choice = input("Select status").strip()

    if choice not in options:
        print("Invalid status option")
        return

    return options[choice]
