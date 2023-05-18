from copy import deepcopy

from patterns.behavioral_patterns.observer import Subject
from patterns.constants import COURSE_TYPES


# порождающий паттерн Прототип
class CoursePrototype:
    # прототип
    def clone(self):
        return deepcopy(self)


class Course(CoursePrototype, Subject):
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)
        self.students = []
        super().__init__()

    def __str__(self):
        return str(self.name)

    def __getitem__(self, item):
        return self.students[item]

    def add_student(self, student):
        self.students.append(student)
        student.courses.append(self)
        self.notify()

    def get_student_count(self):
        return len(self.students)


class InteractiveCourse(Course):
    pass


class RecordCourse(Course):
    pass


class CourseFactory(Course):
    types = {
        COURSE_TYPES["interactive"]: InteractiveCourse,
        COURSE_TYPES["record"]: RecordCourse,
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, course_type, name, category):
        return cls.types[course_type](name, category)


if __name__ == "__main__":
    print(CourseFactory.types.keys())
