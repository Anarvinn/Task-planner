from main import Task, Console


def run_console():
    console = Console()
    while True:
        print("""
==== Планировщик задач ====
Редактор задач: 1
Информация о задачах: 2

Выход: 0""")
        choice = input("Выберите пункт: ")
        if choice == '1':
            edit_task(console)
        elif choice == '2':
            info_tasks(console)
        elif choice == '0':
            break
        else:
            print("Выбран не верный пункт попробуйте снова")


def edit_task(console):
    while True:
        print("""
==== Редактор задач ====
Создать задачу: 1
Редактировать задачу: 2
Добавить зависимость: 3
Удалить зависимость: 4

Выйти: 0
""")
        choice = input("Выберите пункт: ")
        if choice == '1':
            create_task(console)
        elif choice == '2':
            update_task(console)
        elif choice == '3':
            add_dependencies(console)
        elif choice == '4':
            del_dependencies(console)
        elif choice == '0':
            break
        else:
            print("Выбран не верный пункт попробуйте снова")


def info_tasks(console):
    while True:
        print("""
==== Информация о задачах ====
Задачи готовые к реализации: 1
Порядка выполнения всех задач: 2
Информация о конкретной задачи: 3
Выполненые задачи: 4

Выход: 0
""")
        choice = input("Выберите пункт: ")
        if choice == '1':
            ready_task(console)
        elif choice == '2':
            order_of_execution(console)
        elif choice == '3':
            task_info(console)
        elif choice == '4':
            completed_task(console)
        elif choice == '0':
            break
        else:
            print("Выбран не верный пункт попробуйте снова")


def create_task(console):
    while True:
        try:
            print("""
Для создания укажите:
Название задачи
Вариантов приоритета: Высокий/Средний/Низкий
Выход: 0
""")
            title = input("Название задачи: ")
            if title == '0':
                break
            priotity = input("Приоритет: ")
            if priotity == '0':
                break
            console.create_task(title, priotity)
            print("Задача успешно создана")
            break
        except (TypeError, ValueError) as e:
            print(e)


def update_task(console):
    while True:
        print("""
Что вы хотите изменить ?
Название: 1
Приоритет: 2
Статус: 3

Выход: 0
""")
        choice = input("Выберите пункт: ")
        if choice in ['1', '2', '3']:
            id = input("ID изменяемого задачи: ")
            try:
                console.check_id(id)
                value = input("Новое значение: ")
                console.update_task(id, value, choice)
                print("Задача отредактирована")
            except (KeyError, ValueError) as e:
                print(e)
        elif choice == '0':
            break
        else:
            print("Выбран не верный пункт попробуйте снова")


def add_dependencies(console):
    while True:
        try:
            print("Введите ID задачи для которой добавить зависимость")
            id = input('ID: ')
            console.check_id(id)
            print("Введите ID задачи которую хотите добавить в зависимость")
            dependencies = input("ID: ")
            console.check_id(dependencies)
            console.add_dependencies(id, dependencies)
            print("Зависимость успешно добавлена")
            break
        except KeyError as e:
            print(e)


def del_dependencies(console):
    pass


def ready_task(console):
    pass


def order_of_execution(console):
    pass


def task_info(console):
    pass


def completed_task(console):
    pass


if __name__ == '__main__':
    run_console()
