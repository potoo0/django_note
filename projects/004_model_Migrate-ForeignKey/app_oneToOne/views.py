from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from app_oneToOne.models import Person, IDcard


def index(request):
    return HttpResponse('app oneToOne demo index')


def add_person(request: HttpRequest):
    username = request.GET.get('uname')

    person = Person()
    person.p_name = username
    person.save()

    return HttpResponse(f'Person {person.id} created successfully')


def add_idcard(request: HttpRequest):
    id_num = request.GET.get('idnum')

    idcard = IDcard()
    idcard.id_num = id_num
    idcard.save()

    return HttpResponse(f'id card {idcard.id} created successfully')


def bind_idcard(request):
    ''' 每次取最新的 person 和 idcard 进行绑定 '''
    person = Person.objects.last()
    idcard = IDcard.objects.last()

    idcard.id_person = person
    idcard.save()

    return HttpResponse('bind person and idcard successfully')


def remove_person(request: HttpRequest):
    ''' 移除最新的 person '''
    person = Person.objects.last()
    person.delete()

    return HttpResponse('remove person successfully')


def remove_idcard(request: HttpRequest):
    ''' 移除最新的 person '''
    idcard = IDcard.objects.last()
    idcard.delete()

    return HttpResponse('remove idcard successfully')


def get_person_byid(request: HttpRequest):
    idcard = IDcard.objects.last()
    person = idcard.id_person

    return HttpResponse(person.p_name)


def get_idcard_byperson(request: HttpRequest):
    person = Person.objects.last()
    idcard = person.idcard

    return HttpResponse(idcard.id_num)
