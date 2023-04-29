from patterns.constants import USER_TYPES


# Пользователи и покупатели
class User:
    pass


class Customer(User):
    pass


class Employee(User):
    pass


class UserFactory:
    types = {
        USER_TYPES["customer"]: Customer,
        USER_TYPES["employee"]: Employee,
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, user_type):
        return cls.types[user_type]()
