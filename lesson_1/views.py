from wsgi_framework.templator import render


class Index:
    def __call__(self, request):
        return "200 OK", render("index.html", username=request.get("username", None))


class ContactUs:
    def __call__(self, request):
        return "200 OK", render("contact.html", request=request)
