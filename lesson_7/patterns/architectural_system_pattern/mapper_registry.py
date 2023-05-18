from sqlite3 import connect

from patterns.architectural_system_pattern.student_mapper import StudentMapper
from patterns.creation_patterns.user_factory import Student
from settings import PATH_TO_DATABASE

connection = connect(PATH_TO_DATABASE)


class MapperRegistry:
    mappers = {
        "student": StudentMapper,
    }

    @staticmethod
    def get_mapper(obj):
        if isinstance(obj, Student):
            return StudentMapper(connection)

    @staticmethod
    def get_current_mapper(name):
        return MapperRegistry.mappers[name](connection)
