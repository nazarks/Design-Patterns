from quopri import decodestring

from patterns.creation_patterns.category import Category
from patterns.creation_patterns.product_factory import ProductFactory
from patterns.creation_patterns.user_factory import UserFactory


# основной интерфейс проекта
class Engine:
    def __init__(self):
        self.employees = []
        self.customers = []
        self.products = []
        # {'id': categories}
        self.categories = {}

    @staticmethod
    def create_user(user_type):
        return UserFactory.create(user_type)

    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    def find_category_by_id(self, category_id):
        return self.categories.get(category_id, None)

    @staticmethod
    def create_product(product_type, name, category):
        return ProductFactory.create(product_type, name, category)

    def get_product(self, name):
        for product in self.products:
            if product.name == name:
                return product
        return None

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace("%", "=").replace("+", " "), "UTF-8")
        val_decode_str = decodestring(val_b)
        return val_decode_str.decode("UTF-8")
