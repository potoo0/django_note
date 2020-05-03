from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    # print('')
    # print(dir(request))

    # print(f'path: {request.path}\n')
    # print(f'method: {request.method}\n')
    # print(f'encoding: {request.encoding}\n')

    # print(f'GET: {request.GET}, type: {type(request.GET)}\n')
    # print(f'POST: {request.POST}, type: {type(request.POST)}\n')
    # print(f'FILES: {request.FILES}, type: {type(request.FILES)}\n')
    # print(f'COOKIES: {request.COOKIES}, type: {type(request.COOKIES)}\n')
    # print(f'session: {request.session}, type: {type(request.session)}\n')

    # print(f'get: {request.GET.get("a")}')
    # print(f'getlist{request.GET.getlist("a")}')

    # print(f'META type: {type(request.META)}, content:')
    # for key in request.META:
    #     print(f'{key}: {request.META.get(key)}')
    return render(request, 'app_url.html')


def hello(request):
    return HttpResponse('hello')


def hellooo(request):
    return HttpResponse('hellooo')


def geturlarg(request, id_int):
    info = f'id_int: {id_int}, type: {type(id_int).__name__}'
    return HttpResponse(info)


def geturlargs_p(request, arg1, arg2):
    info = f'position arg:\narg1: {arg1}, arg2: {arg2}, type: {type(arg1).__name__}'
    return HttpResponse(info)


def geturlargs_k(request, arg1, arg2):
    info = f'key arg:\narg1: {arg1}, arg2: {arg2}, type: {type(arg1).__name__}'
    return HttpResponse(info)
