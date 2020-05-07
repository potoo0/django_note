from django.shortcuts import render
from django.http import HttpResponse
# from app_manyToMany.models import Grade, Student


def index(request):
    return HttpResponse('app many to many index')
