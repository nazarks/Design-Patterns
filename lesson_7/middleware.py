import json
from datetime import date


# Получить имя пользователя из сессии
def set_username(request):
    with open(".session") as file:
        session = json.load(file)
    request["username"] = session.get("username", None)


def set_date(request):
    request["date"] = date.today()


fronts = [set_username, set_date]
