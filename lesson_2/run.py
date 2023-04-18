from middleware import fronts
from urls import routes
from wsgi_framework.core import Framework

application = Framework(routes, fronts)


if __name__ == "__main__":
    # Запуск gunicorn с параметрами application -b 127.0.0.1:8080 --reload

    import multiprocessing

    import gunicorn.app.base

    def number_of_workers():
        return (multiprocessing.cpu_count() * 2) + 1

    class StandaloneApplication(gunicorn.app.base.BaseApplication):
        def __init__(self, app, options=None):
            self.options = options or {}
            self.application = app
            super().__init__()

        def load_config(self):
            config = {
                key: value for key, value in self.options.items() if key in self.cfg.settings and value is not None
            }
            for key, value in config.items():
                self.cfg.set(key.lower(), value)

        def load(self):
            return self.application

    options = {"bind": "%s:%s" % ("127.0.0.1", "8080"), "workers": number_of_workers(), "reload": True}

    StandaloneApplication(application, options).run()
