from copy import deepcopy

from patterns.constants import PRODUCT_TYPES


# порождающий паттерн Прототип
class ProductPrototype:
    # прототип
    def clone(self):
        return deepcopy(self)


class Product(ProductPrototype):
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.products.append(self)


# Товар
class Goods(Product):
    pass


# Услуга
class Service(Product):
    pass


class ProductFactory(Product):
    types = {
        PRODUCT_TYPES["goods"]: Goods,
        PRODUCT_TYPES["service"]: Service,
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, product_type, name, category):
        return cls.types[product_type](name, category)


if __name__ == "__main__":
    print(ProductFactory.types.keys())
