from django.shortcuts import render
from django.http import HttpResponse
from app_oneToMany.models import Grade, Student


def index(request):
    return HttpResponse('app one to many index')
