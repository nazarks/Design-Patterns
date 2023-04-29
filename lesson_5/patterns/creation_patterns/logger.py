from datetime import datetime
from os import path


# порождающий паттерн Синглтон
class SingletonByName(type):
    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs["name"]

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):
    def __init__(self, name, log_dir):
        self.name = name
        self.log_dir = log_dir

    # @staticmethod
    def log(self, text):
        print(datetime.utcnow(), text)
        file_name = path.join(self.log_dir, self.name)
        with open(file_name, mode="a", encoding="utf-8") as file:
            file.write(f"{datetime.utcnow()}: {text}\n")
