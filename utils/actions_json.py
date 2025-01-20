import json


class ActionsJSON(dict):
    def __init__(self):
        # Инициализируем словарь с двумя ключами и пустыми списками в качестве значений
        super().__init__({
            "messages": [],
            "commands": []
        })

    def __setitem__(self, key, value):
        # Разрешаем изменять только ключи "message" и "commands"
        if key not in ["messages", "commands"]:
            raise KeyError(f"Key '{key}' is not allowed. Only 'message' and 'commands' are valid keys.")

        # Проверяем, что значение является списком строк
        if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
            raise ValueError(f"Value for key '{key}' must be a list of strings.")

        # Устанавливаем значение
        super().__setitem__(key, value)

    def to_json(self):
        return json.dumps(self, ensure_ascii=False)

    def add_message(self, message: str):
        self["messages"].append(message)

    def add_command(self, command: str):
        self["commands"].append(command)

    def get_messages(self):
        return self["messages"]

    def get_commands(self):
        return self["commands"]

    @classmethod
    def from_json(cls, json_data):
        if isinstance(json_data, str):
            json_data = json.loads(json_data)

        obj = cls()

        # Заполняем объект данными из словаря
        for key, value in json_data.items():
            if key in obj:  # Проверяем, что ключ допустим
                obj[key] = value  # Используем __setitem__ для проверки значения

        return obj
