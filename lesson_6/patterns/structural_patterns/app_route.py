from wsgi_framework.core import flask_routes


# структурный паттерн декоратор
class AppRoute:
    def __init__(self, url):
        self.routes = flask_routes
        self.url = url

    def __call__(self, cls):
        self.routes[self.url] = cls()
