from main import Task


def run_console():
    while True:
        print("""
==== Планировщик задач ====
Редактор задач: 1
Информация о задачах: 2

Выход: 0""")
        choice = input("Выберите пункт: ")
        if choice == '1':
            edit_task()
        elif choice == '2':
            info_task()
        elif choice == '0':
            break
        else:
            print("Выбран не верный пункт попробуйте снова")


def edit_task():
    pass


def info_task():
    pass


if __name__ == '__main__':
    run_console()
