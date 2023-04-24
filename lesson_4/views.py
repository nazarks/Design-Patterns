import json
import os
import time

from patterns.constants import PRODUCT_TYPES
from patterns.creation_patterns.logger import Logger
from patterns.engine import Engine
from settings import LOG_DIR, MESSAGES_DIR
from wsgi_framework.templator import render

site = Engine()
logger = Logger("main", LOG_DIR)


class Index:
    def __call__(self, request):
        return "200 OK", render("index.html", objects_list=site.categories.values(), request=request)


class ContactUs:
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


class CreateCategory:
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


class ProductList:
    def __call__(self, request):
        category_id = request["get_params"].get("category_id", None)
        category = None
        if category_id:
            category_id = int(category_id)
            category = site.find_category_by_id(category_id)

        if category:
            logger.log(f"Список товаров и услуг для категории {category.name}")
            return "200 OK", render(
                "product_list.html", objects_list=category.products, name=category.name, id=category.id, request=request
            )
        return "200 OK", render("index.html", objects_list=site.categories.values(), request=request)


class CreateProduct:
    category_id = -1

    def __call__(self, request):
        if request["method"] == "POST":
            # метод POST
            name = request["post_params"].get("name", None)
            name = site.decode_value(name)
            if not name:
                return "200 OK", render("index.html", objects_list=site.categories.values(), request=request)

            product_type = request["post_params"].get("product_type", None)
            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))

                product = site.create_product(product_type, name, category)
                site.products.append(product)
                logger.log(f"Добавлен товар: {product.name}")

            return "200 OK", render(
                "product_list.html", objects_list=category.products, name=category.name, id=category.id, request=request
            )

        # метод GET
        self.category_id = int(request["get_params"]["id"])
        category = site.find_category_by_id(int(self.category_id))
        if category:
            return "200 OK", render(
                "create_product.html",
                name=category.name,
                id=category.id,
                product_types=PRODUCT_TYPES.values(),
                request=request,
            )
        return "200 OK", render("index.html", objects_list=site.categories.values(), request=request)


class CopyProduct:
    def __call__(self, request):
        name = request["get_params"].get("name", None)
        name = site.decode_value(name)
        if name:
            old_product = site.get_product(name)
            if old_product:
                new_name = f"copy_{name}"
                new_product = old_product.clone()
                new_product.name = new_name
                # добавим новый объект в список объектов категории
                category = site.find_category_by_id(new_product.category.id)
                category.products.append(new_product)

                # добавить объект на сайт
                site.products.append(new_product)

                logger.log(f"Скопировано: {new_product.name}, категория: {category.name}")
                return "200 OK", render(
                    "product_list.html",
                    objects_list=category.products,
                    name=category.name,
                    id=category.id,
                    request=request,
                )

        return "200 OK", render("index.html", objects_list=site.categories.values(), request=request)


class About:
    def __call__(self, request):
        return "200 OK", render("about.html", request=request)
