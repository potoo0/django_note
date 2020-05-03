from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpRequest, JsonResponse
# Create your views here.
from app_token.models import Student
from django.db.models import Q

from time import ctime
import hashlib


def index(request):
    return HttpResponse('token demo index')


def register(request: HttpRequest):
    if request.method == 'GET':
        return render(request, 'app_token_reg.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            student = Student()

            student.s_name = username
            student.s_password = password

            student.save()
        except Exception:
            return redirect(reverse('app_token:register'))

        return HttpResponse('注册成功')


def generate_token(ip, username):
    '''generate unique token'''
    c_time = ctime()
    r = username

    token = hashlib.new('md5', (ip + c_time + r).encode('utf-8')).hexdigest()

    return token


def login(request: HttpRequest):
    if request.method == "GET":
        return render(request, 'app_token_login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        students = Student.objects.filter(
            Q(s_name=username) & Q(s_password=password))

        if students.exists():
            student = students.first()

            ip = request.META.get('REMOTE_ADDR')
            token = generate_token(ip, username)
            student.s_token = token
            student.save()

            # response = HttpResponse('登陆成功')
            # response.set_cookie('token', token)
            # return response
            data = {
                "status": 200,
                "msg": "login success",
                "token": token
            }
            return JsonResponse(data=data)
        # return redirect(reverse('app_token:login'))
        data = {
            "status": 800,
            "msg": "verify failed",
        }
        return JsonResponse(data=data)


def logged(request: HttpRequest):
    # token = request.COOKIES.get('token')
    token = request.GET.get('token')
    try:
        student = Student.objects.get(s_token=token)
    except Student.DoesNotExist:
        return redirect(reverse('app_token:login'))
    # return HttpResponse(student.s_name)
    data = {
        "status": 200,
        "msg": "ok",
        "data": {
            'username': student.s_name
        }
    }
    return JsonResponse(data=data)
