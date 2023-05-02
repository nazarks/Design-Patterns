import json
import os
import time

from patterns.behavioral_patterns.cbv import CreateView, ListView
from patterns.behavioral_patterns.observer import EmailNotifier, SmsNotifier
from patterns.behavioral_patterns.serializers import BaseSerializer
from patterns.behavioral_patterns.writers import FileWriter
from patterns.constants import COURSE_TYPES, USER_TYPES
from patterns.creation_patterns.logger import Logger
from patterns.engine import Engine
from patterns.structural_patterns.app_route import AppRoute
from patterns.structural_patterns.debug import Debug
from settings import MESSAGES_DIR, PATH_TO_LOG
from wsgi_framework.templator import render

__all__ = [
    "Index",
]

site = Engine()
logger = Logger("main", FileWriter(PATH_TO_LOG))
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()


@AppRoute(url="/")
class Index:
    @Debug()
    def __call__(self, request):
        return "200 OK", render("index.html", objects_list=site.categories.values(), request=request)


@AppRoute(url="/about/")
class About:
    @Debug()
    def __call__(self, request):
        return "200 OK", render("about.html", request=request)


@AppRoute(url="/contact/")
class ContactUs:
    @Debug()
    def __call__(self, request):
        method = request.get("method", "GET")
        form = {}
        if method == "POST":
            # Получаем данные формы
            topic = request["post_params"].get("topic", None)
            email = request["post_params"].get("email", None)
            message = request["post_params"].get("message", None)
            form = {"email": email, "topic": topic, "message": message}
            if topic and email and message:
                # Данные есть записываем в файл
                file_name = os.path.join(MESSAGES_DIR, email + "_" + str(time.time()))
                with open(file_name, "w", encoding="utf-8") as file:
                    json.dump(obj=form, fp=file, ensure_ascii=False)
                form["result"] = "Данные успешно отправлены"
                form["message"] = ""
            else:
                form["error"] = "Форма заполнена неверно"

        # Рендер пустой (метод GET) или заполненной (метод POST) формы
        return "200 OK", render("contact.html", request=request, form=form)


@AppRoute(url="/create-category/")
class CreateCategory:
    @Debug()
    def __call__(self, request):
        if request["method"] == "POST":
            # метод пост

            name = request["post_params"].get("name", None)
            name = site.decode_value(name)
            if not name:
                return "200 OK", render("index.html", objects_list=site.categories.values(), request=request)

            parent_category_id = request["post_params"].get("parent_category_id", None)
            category = None
            if parent_category_id:
                category = site.find_category_by_id(int(parent_category_id))
            if category:
                logger.log(f"Создаем подкатегорию для категории {category.name}")
            else:
                logger.log(f"Создаем категорию {name}")
            new_category = site.create_category(name, category)
            site.categories[new_category.id] = new_category
            return "200 OK", render("index.html", objects_list=site.categories.values(), request=request)
        else:
            parent_category_id = request["get_params"].get("parent_category_id", None)
            categories = site.categories.values()

            return "200 OK", render(
                "create_category.html", categories=categories, parent_category_id=parent_category_id, request=request
            )


@AppRoute(url="/course-list/")
class CourseList:
    def __call__(self, request):
        category_id = request["get_params"].get("category_id", None)
        category = None
        if category_id:
            category_id = int(category_id)
            category = site.find_category_by_id(category_id)

        if category:
            logger.log(f"Список курсов для категории {category.name}")
            return "200 OK", render(
                "course_list.html", objects_list=category.courses, name=category.name, id=category.id, request=request
            )
        return "200 OK", render("index.html", objects_list=site.categories.values(), request=request)


@AppRoute(url="/create-course/")
class CreateCourse:
    category_id = -1

    def __call__(self, request):
        if request["method"] == "POST":
            # метод POST
            name = request["post_params"].get("name", None)
            name = site.decode_value(name)
            if not name:
                return "200 OK", render("index.html", objects_list=site.categories.values(), request=request)

            course_type = request["post_params"].get("course_type", None)
            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))

                course = site.create_course(course_type, name, category)
                course.observers.append(email_notifier)
                course.observers.append(sms_notifier)
                site.courses.append(course)
                logger.log(f"Добавлен курс: {course.name}")

            return "200 OK", render(
                "course_list.html", objects_list=category.courses, name=category.name, id=category.id, request=request
            )

        # метод GET
        self.category_id = int(request["get_params"]["id"])
        category = site.find_category_by_id(int(self.category_id))
        if category:
            return "200 OK", render(
                "create_course.html",
                name=category.name,
                id=category.id,
                course_types=COURSE_TYPES.values(),
                request=request,
            )
        return "200 OK", render("index.html", objects_list=site.categories.values(), request=request)


@AppRoute(url="/copy-course/")
class CopyCourse:
    @Debug()
    def __call__(self, request):
        name = request["get_params"].get("name", None)
        name = site.decode_value(name)
        if name:
            old_course = site.get_course(name)
            if old_course:
                new_name = f"copy_{name}"
                new_course = old_course.clone()
                new_course.name = new_name
                # добавим новый объект в список объектов категории
                category = site.find_category_by_id(new_course.category.id)
                category.courses.append(new_course)

                # добавить объект на сайт
                site.courses.append(new_course)

                logger.log(f"Скопировано: {new_course.name}, категория: {category.name}")
                return "200 OK", render(
                    "course_list.html",
                    objects_list=category.courses,
                    name=category.name,
                    id=category.id,
                    request=request,
                )

        return "200 OK", render("index.html", objects_list=site.categories.values(), request=request)


@AppRoute(url="/student-list/")
class StudentList(ListView):
    queryset = site.students
    template_name = "student_list.html"


@AppRoute(url="/create-student/")
class StudentCreateView(CreateView):
    template_name = "create_student.html"

    def __init__(self):
        super().__init__()
        self.new_obj = None

    def create_obj(self, data: dict):
        name = data["name"]
        name = site.decode_value(name)
        new_obj = site.create_user(USER_TYPES["student"], name)
        site.students.append(new_obj)

        # Добавим в шаблон уведомление, что пользователь создан успешно
        self.new_obj = new_obj
        logger.log(f"Добавлен студент: {new_obj.name}")

    def get_context_data(self):
        context = super().get_context_data()
        context["new_user"] = self.new_obj
        return context

    def __call__(self, *args, **kwargs):
        self.new_obj = None
        return super().__call__(*args, **kwargs)


@AppRoute(url="/add-student/")
class AddStudentByCourseCreateView(CreateView):
    template_name = "add_student.html"

    def __init__(self):
        super().__init__()
        self.student = None
        self.course = None

    def get_context_data(self):
        context = super().get_context_data()
        context["courses"] = site.courses
        context["students"] = site.students
        context["student"] = self.student
        context["course"] = self.course
        return context

    def create_obj(self, data: dict):
        course_name = data.get("course_name", None)
        student_name = data.get("student_name", None)
        if not (course_name and student_name):
            return
        course_name = site.decode_value(course_name)
        course = site.get_course(course_name)
        student_name = site.decode_value(student_name)
        student = site.get_student(student_name)
        course.add_student(student)
        # Информация о добавлении студента в курс
        logger.log(f"Добавлен студент: {student} на курс: {course}")
        self.student = student
        self.course = course

    def __call__(self, *args, **kwargs):
        self.student = None
        self.course = None
        return super().__call__(*args, **kwargs)


@AppRoute(url="/students-by-course/")
class StudentByCourseList(ListView):
    queryset = site.courses
    template_name = "students_by_course.html"


@AppRoute(url="/api/")
class CourseApi:
    @Debug()
    def __call__(self, request):
        return "200 OK", BaseSerializer(site.courses).save()
