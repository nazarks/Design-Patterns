from patterns.architectural_system_pattern.domain import DomainObject
from patterns.constants import USER_TYPES


# Пользователи и покупатели
class User:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return str(self.name)


class Teacher(User):
    pass


class Student(User, DomainObject):
    def __init__(self, name):
        self.courses = []
        super().__init__(name)


class UserFactory:
    types = {
        USER_TYPES["student"]: Student,
        USER_TYPES["teacher"]: Teacher,
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, user_type, name):
        return cls.types[user_type](name)
