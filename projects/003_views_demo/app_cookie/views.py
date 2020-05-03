from django.shortcuts import render, redirect
from django.http import HttpResponse
# from django.http.request import QueryDict
# from django.utils.datastructures import MultiValueDict
from django.http import HttpResponseRedirect, JsonResponse
from django.http import HttpRequest
from django.urls import reverse
from datetime import datetime, timedelta


# Create your views here.
def response_(request):
    response = HttpResponse()

    # response.content = 'response_'
    # response.status_code = 404
    response.write('response.write')

    return response


def respRedirect(request):
    # direct url
    # return HttpResponseRedirect('/app/index')

    # reverse url
    url = reverse('app_url:index')
    print(url)
    return redirect(url)


def getjson(request):
    fakeJson = {'day': 2020, 'month': 'March'}
    return JsonResponse(fakeJson)


def setcookie(request):
    response = HttpResponse('set cookie')
    response.set_cookie('username', 'Rick')

    return response


def getcookie(request: HttpRequest):
    username = request.COOKIES.get('username')
    return HttpResponse(username)


def login(request):
    return render(request, 'app_cookie_login.html')


def do_login(request: HttpRequest):
    # 实际上，一般将这部分也写到 login 视图中，通过 request.method 来区分请求。这样登陆就具有了内聚特点
    username = request.POST.get('username')

    response = redirect(reverse('app_cookie:logged'))
    # response.set_cookie(
    #     'username', username,
    #     max_age=20,
    #     # expires=datetime.now() + timedelta(seconds=20),
    # )
    response.set_signed_cookie(
        'username', username,
        salt='salt',
        # max_age=50,
    )
    # response.set_signed_cookie(
    #     'username', username,
    #     salt='salt',
    #     max_age=50,
    # )

    return response


def logged(request: HttpRequest):
    try:
        # username = request.COOKIES.get('username')
        username = request.get_signed_cookie('username', salt='salt')

        if username:
            return render(request, 'app_cookie_logged.html',
                          context={'username': username})
    except Exception:
        pass
    return redirect(reverse('app_cookie:login'))


def logout(request):
    response = redirect(reverse('app_cookie:login'))
    response.delete_cookie('username')

    return response
