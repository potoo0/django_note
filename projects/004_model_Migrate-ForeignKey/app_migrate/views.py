from django.shortcuts import render
from django.http import HttpResponse, HttpRequest


def index(request):
    return HttpResponse('app migrate demo index')
