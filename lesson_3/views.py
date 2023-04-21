import json
import os
import time

from settings import MESSAGES_DIR
from wsgi_framework.templator import render


class Index:
    def __call__(self, request):
        return "200 OK", render("index.html", username=request.get("username", None))


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
