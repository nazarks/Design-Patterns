from wsgi_framework.request_middleware import framework_fronts


class PageNotFound404:
    def __call__(self, request):
        return "404 WHAT", "404 PAGE Not Found"


class Framework:
    """Класс Framework - основа фреймворка"""

    def __init__(self, routes_obj, fronts_obj):
        self.routes = routes_obj
        self.fronts = fronts_obj
        self.framework_fronts = None

        self.init_middleware()

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

        request = {}
        # наполняем словарь request элементами этот словарь получат все контроллеры
        # middleware установленные по умолчанию
        for front in self.framework_fronts:
            front(request=request, environ=environ)

        # пользовательский middleware отработка паттерна front controller
        for front in self.fronts:
            front(request)

        # запуск контроллера с передачей объекта request
        code, body = view(request)
        start_response(code, [("Content-Type", "text/html")])
        return [body.encode("utf-8")]
