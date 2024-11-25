from django.http import HttpResponse
from django.shortcuts import render

from app.models import Executive


def index(request):
    executive = Executive.objects.first()

    if executive:
        print(executive)
    else:
        print("Executive not found")
    return HttpResponse("Hello, world.")
