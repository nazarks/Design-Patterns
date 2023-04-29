from wsgi_framework.request_middleware import framework_fronts

flask_routes = {}


class PageNotFound404:
    def __call__(self, request):
        return "404 WHAT", "404 PAGE Not Found"


class Framework:
    """Класс Framework - основа фреймворка"""

    def __init__(self, fronts_obj):
        self.routes = None
        self.fronts = fronts_obj
        self.framework_fronts = None
        self.request = {}

        self.init_middleware()
        self.init_routes()

    def init_routes(self):
        self.routes = flask_routes

    def init_middleware(self):
        self.framework_fronts = framework_fronts

    def __call__(self, environ, start_response):
        # получаем адрес, по которому выполнен переход
        path = environ["PATH_INFO"]

        # добавление закрывающего слеша
        if not path.endswith("/"):
            path = f"{path}/"

        # находим нужный контроллер отработка паттерна page controller
        if path in self.routes:
            view = self.routes[path]
        else:
            view = PageNotFound404()

        # request = {}
        # наполняем словарь request элементами этот словарь получат все контроллеры
        # middleware установленные по умолчанию
        for front in self.framework_fronts:
            front(request=self.request, environ=environ)

        # пользовательский middleware отработка паттерна front controller
        for front in self.fronts:
            front(self.request)

        # запуск контроллера с передачей объекта request
        code, body = view(self.request)
        start_response(code, [("Content-Type", "text/html")])
        return [body.encode("utf-8")]


# Debug WSGI-application
class DebugApplication(Framework):
    def __init__(self, fronts_obj):
        self.app = Framework(fronts_obj=fronts_obj)
        super().__init__(fronts_obj)

    def __call__(self, env, start_response):
        result = self.app(env, start_response)
        print(
            f"Debug --> Метод {env['REQUEST_METHOD']} POST параметры: {self.app.request.get('post_params', None)},"
            f" GET параметры {self.app.request.get('get_params', None)}",
        )
        return result


# Fake WSGI-application
class FakeApplication(Framework):
    def __init__(self, fronts_obj):
        self.app = Framework(fronts_obj=fronts_obj)
        super().__init__(fronts_obj)

    def __call__(self, env, start_response):
        start_response("200 OK", [("Content-Type", "text/html")])
        return [b"Hello from Fake"]


class ApplicationFactory:
    types = {
        "default": Framework,
        "debug": DebugApplication,
        "fake": FakeApplication,
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, application_type, fronts):
        return cls.types[application_type](fronts)
