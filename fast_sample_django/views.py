from django.http import HttpResponse


def health():
    return HttpResponse("Hello, world. You're at the polls index.")

