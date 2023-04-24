class Category:
    auto_id = 0

    def __init__(self, name, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        # родительская категория
        self.category = category
        # список продуктов категории
        self.products = []

    def product_count(self):
        count = len(self.products)
        return count
