from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.template import loader
from app_middleware.models import Student
from django.contrib.sessions.middleware import SessionMiddleware


def index(request):
    # testModelError = Student.objects.get(pk=11)
    # raise Exception('exception in view')
    # return render(request, 'app_mw_index.html')
    # template = loader.get_template('app_mw_index.html')
    # return template
    return render(request, 'app_mw_index.html')


def testaop1(request):
    return HttpResponse('aop1')


def testaop2(request):
    return HttpResponse('aop2')
