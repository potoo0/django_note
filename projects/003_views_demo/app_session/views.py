from django.shortcuts import render, redirect, reverse
from django.http import HttpRequest, HttpResponse


def index(request: HttpRequest):
    print(help(request.session.set_expiry))
    return HttpResponse('session demo index')


def login(request: HttpRequest):
    if request.method == 'GET':
        return render(request, 'app_session_login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')

        request.session['username'] = username
        request.session.set_expiry(600)

        return redirect(reverse('app_session:logged'))


def logged(request: HttpRequest):
    username = request.session.get('username')

    if username:
        return render(request, 'app_session_logged.html',
                      context={'username': username})
    # except Exception as e:
    #     pass
    return redirect(reverse('app_session:login'))


def logout(request: HttpRequest):
    response = redirect(reverse('app_session:login'))

    # wrong
    # response.delete_cookie('sessionid')
    # del request.session['username']

    # correct
    # request.session.flush()
    # request.session.clear()

    print(request.session.session_key)

    return response
