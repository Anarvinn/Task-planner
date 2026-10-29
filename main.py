import uuid
import re


class Task:
    def __init__(self, title, priority, id=None):
        self.id = (id, str(uuid.uuid4()))[id is None]
        self.title = title
        self.priority = priority
        self.status = "Новая"
        self.task_list = []

    def __setattr__(self, name, value):
        if name in ['title', 'priotity', 'status']:
            if not isinstance(value, str):
                raise TypeError(f"Значением для {name} должны быть строкой")

            if name == 'priority':
                if not value in ['Высокий', 'Средний', 'Низкий']:
                    raise ValueError(
                        "Указан неверный вариант. Укажите один из вариантов: 'Высокий', 'Средний', 'Низкий'")

            elif name == 'status':
                if not value in ['Новая', 'В работе', 'Завершена']:
                    raise ValueError(
                        "Указан неверный вариант. Укажите один из вариантов: 'Новая', 'В работе', 'Завершена'")
        super().__setattr__(name, value)

    def __str__(self):
        return f"{self.title}, {self.priority}, {self.status}, {self.task_list}, {self.id}"

    def change_dependencies(self, id_task, flag=True):
        try:
            self.chek_id(id_task)
        except (ValueError, TypeError, AttributeError):
            print("Указан некорректный ID")
        if flag:
            self.task_list.append(id_task)
        else:
            try:
                self.task_list.pop(id_task)
            except ValueError:
                print("Указаной задачи нет в списке")

    @staticmethod
    def chek_id(id):
        try:
            uuid.UUID(str(id))
            return True
        except (ValueError, TypeError, AttributeError):
            raise
