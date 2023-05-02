from wsgiref.simple_server import make_server

from middleware import fronts
from views import *
from wsgi_framework.core import ApplicationFactory

# APPLICATION_TYPE: default, debug, fake,
APPLICATION_TYPE = "default"


application = ApplicationFactory.create(APPLICATION_TYPE, fronts)

if __name__ == "__main__":
    with make_server("", 8080, application) as httpd:
        print("Запуск на порту 8080...")
        httpd.serve_forever()
