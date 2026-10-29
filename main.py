import uuid
import json


class Console:

    def create_task(self, title, priority):
        task = Task(title, priority)
        id = task.id
        data = self.get_data()
        data[id] = self.json_serialize(task)
        self.save_data(data)

    def update_task(self, id, value, key):
        help_dict = {'1': 'title',
                     '2': 'priority',
                     '3': 'status'}
        key = help_dict[key]
        data = self.get_data()
        task = Task(id=id, **data[id])
        task.__setattr__(key, value)
        data[id] = self.json_serialize(task)
        self.save_data(data)

    def add_dependencies(self, id, dependencies):
        pass

    def save_data(self, data):
        with open('data.json', 'w', encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
            file.write('\n')

    def get_data(self):
        try:
            with open('data.json', 'r', encoding="utf-8") as file:
                data = json.load(file)
                if not data:
                    raise json.JSONDecodeError
                return data
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def check_id(self, id):
        data = self.get_data()
        if not data.get(id):
            raise KeyError("Нет задачи с таким ID")

    def json_serialize(self, task):
        data = task.__dict__
        data.pop('id')
        return data


class Task:
    def __init__(self, title, priority, status=None, task_list=None, id=None):
        self.id = (id, str(uuid.uuid4()))[id is None]
        self.title = title
        self.priority = priority
        self.status = (status, "Новая")[status is None]
        self.task_list = (task_list, [])[task_list is None]

    def __setattr__(self, name, value):
        if name in ['title', 'priority', 'status']:
            if not isinstance(value, str):
                raise TypeError(f"Значением для {name} должны быть строкой")

            if name == 'priority':
                if value not in ['Высокий', 'Средний', 'Низкий']:
                    raise ValueError(
                        "Указан неверный приоритет. Укажите один из вариантов: 'Высокий', 'Средний', 'Низкий'")

            elif name == 'status':
                if not value in ['Новая', 'В работе', 'Завершена']:
                    raise ValueError(
                        "Указан неверный статус. Укажите один из вариантов: 'Новая', 'В работе', 'Завершена'")
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
