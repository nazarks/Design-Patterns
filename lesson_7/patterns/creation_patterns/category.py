class Category:
    auto_id = 0

    def __init__(self, name, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        # родительская категория
        self.category = category
        # список продуктов категории
        self.courses = []

    def course_count(self):
        count = len(self.courses)
        return count

    def __str__(self):
        return f"Категория: {self.name}, родительская категория {self.category}"
