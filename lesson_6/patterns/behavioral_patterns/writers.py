from datetime import datetime


# поведенческий паттерн - Стратегия
class ConsoleWriter:
    @staticmethod
    def write(text):
        print(f"{datetime.utcnow()}: {text}\n")


class FileWriter:
    def __init__(self, path_to_file):
        self.file_name = path_to_file

    def write(self, text):
        with open(self.file_name, "a", encoding="utf-8") as f:
            f.write(f"{text}\n")
