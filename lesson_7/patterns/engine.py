from quopri import decodestring

from patterns.architectural_system_pattern.mapper_registry import MapperRegistry
from patterns.architectural_system_pattern.unit_of_work import UnitOfWork
from patterns.creation_patterns.category import Category
from patterns.creation_patterns.course_factory import CourseFactory
from patterns.creation_patterns.user_factory import UserFactory

UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)


# основной интерфейс проекта
class Engine:
    def __init__(self):
        self.students = []
        self.teachers = []
        self.courses = []
        # {'id': categories}
        self.categories = {}

        self.load_students()

    def load_students(self):
        mapper = MapperRegistry.get_current_mapper("student")
        self.students = mapper.all()

    @staticmethod
    def create_user(user_type, name):
        return UserFactory.create(user_type, name)

    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    def find_category_by_id(self, category_id):
        return self.categories.get(category_id, None)

    @staticmethod
    def create_course(course_type, name, category):
        return CourseFactory.create(course_type, name, category)

    def get_course(self, name):
        for course in self.courses:
            if course.name == name:
                return course
        return None

    def get_student(self, name):
        for item in self.students:
            if item.name == name:
                return item

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace("%", "=").replace("+", " "), "UTF-8")
        val_decode_str = decodestring(val_b)
        return val_decode_str.decode("UTF-8")
