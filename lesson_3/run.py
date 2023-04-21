from wsgiref.simple_server import make_server

from middleware import fronts
from urls import routes
from wsgi_framework.core import Framework

application = Framework(routes, fronts)


if __name__ == "__main__":
    with make_server("", 8080, application) as httpd:
        print("Запуск на порту 8080...")
        httpd.serve_forever()
