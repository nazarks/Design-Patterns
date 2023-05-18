from datetime import datetime
from os import path

from patterns.behavioral_patterns.writers import FileWriter


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
    def __init__(self, name, writer=FileWriter("log")):
        self.name = name
        self.writer = writer

    # @staticmethod
    def log(self, text):
        self.writer.write(f"{datetime.utcnow()}: {self.name} {text}")
