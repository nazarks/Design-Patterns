# поведенческий паттерн - Шаблонный метод
from wsgi_framework.templator import render


class TemplateView:
    template_name = "template.html"

    def __init__(self):
        self.request = None

    def get_context_data(self):
        return {"request": self.request}

    def get_template(self):
        return self.template_name

    def render_template_with_context(self):
        template_name = self.get_template()
        context = self.get_context_data()
        return "200 OK", render(template_name, **context)

    def __call__(self, request):
        self.request = request
        return self.render_template_with_context()


class ListView(TemplateView):
    queryset = []
    template_name = "list.html"
    context_object_name = "objects_list"

    def get_queryset(self):
        return self.queryset

    def get_context_object_name(self):
        return self.context_object_name

    def get_context_data(self):
        queryset = self.get_queryset()
        context_object_name = self.get_context_object_name()
        context = {context_object_name: queryset, "request": self.request}
        return context


class CreateView(TemplateView):
    template_name = "create.html"

    def get_request_data(self):
        return self.request["post_params"]

    def create_obj(self, data):
        pass

    def __call__(self, request):
        self.request = request
        if request["method"] == "POST":
            # метод пост
            data = self.get_request_data()
            self.create_obj(data)

            return self.render_template_with_context()
        else:
            return super().__call__(request)
