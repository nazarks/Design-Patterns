import json
from quopri import decodestring


def set_get_params(request, environ):
    """Функция добавляет в request параметры GET запроса и сам метод"""
    method = environ["REQUEST_METHOD"]
    if method != "GET":
        return
    request["method"] = method

    # получаем параметры запроса
    query_string = environ["QUERY_STRING"]
    # превращаем параметры в словарь
    request_params = parse_input_data(query_string)
    print(request_params)
    request["get_params"] = decode_value(request_params)
    print(f"Нам пришёл get-запрос: {request['get_params']}")


def set_post_params(request, environ):
    """Функция добавляет в request параметры POST запроса и сам метод"""

    def get_wsgi_input_data(env) -> bytes:
        # получаем длину тела
        content_length_data = env.get("CONTENT_LENGTH")
        # приводим к int
        content_length = int(content_length_data) if content_length_data else 0
        print(content_length)
        # считываем данные, если они есть
        # env['wsgi.input'] -> <class '_io.BufferedReader'>
        # запускаем режим чтения

        data = env["wsgi.input"].read(content_length) if content_length > 0 else b""
        return data

    def parse_wsgi_input_form_data(data: bytes) -> dict:
        result = {}
        if data:
            # декодируем данные
            data_str = data.decode(encoding="utf-8")
            print(f"строка после декодирования - {data_str}")
            # собираем их в словарь
            result = parse_input_data(data_str)
        return result

    def parse_wsgi_input_json_data(data: bytes) -> dict:
        result = {}
        if data:
            # декодируем данные
            data_str = data.decode(encoding="utf-8")
            print(f"строка после декодирования - {data_str}")
            # собираем их в словарь
            result = json.loads(data_str)
        return result

    # проверяем метод
    method = environ["REQUEST_METHOD"]
    if method != "POST":
        return

    request["method"] = method
    # получаем данные
    if "application/json" in environ["CONTENT_TYPE"]:
        data = get_wsgi_input_data(environ)
        data = parse_wsgi_input_json_data(data)
        request["post_params"] = decode_value(data)
        print(f"Нам пришёл post-запрос: {request['post_params']} и CONTENT_TYPE = application/json")

    if "application/x-www-form-urlencoded" in environ["CONTENT_TYPE"]:
        data = get_wsgi_input_data(environ)
        post_params = parse_wsgi_input_form_data(data)
        request["post_params"] = decode_value(post_params)
        print(f"Нам пришёл post-запрос: {request['post_params']} и CONTENT_TYPE = application/x-www-form-urlencoded")


# Общие функции
def parse_input_data(data: str):
    result = {}
    if data:
        # делим параметры через &
        params = data.split("&")
        for item in params:
            # делим ключ и значение через =
            k, v = item.split("=")
            result[k] = v
    return result


def decode_value(data):
    new_data = {}
    for k, v in data.items():
        val = bytes(v.replace("%", "=").replace("+", " "), "UTF-8")
        val_decode_str = decodestring(val).decode("UTF-8")
        new_data[k] = val_decode_str
    return new_data


framework_fronts = [set_get_params, set_post_params]
