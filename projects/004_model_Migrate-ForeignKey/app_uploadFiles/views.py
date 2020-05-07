from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from app_uploadFiles.models import UserModel

def index(request):
    return HttpResponse('upload files index')


def upload(request: HttpRequest):
    if request.method == 'GET':
        return render(request, 'app_upload.html')
    elif request.method == 'POST':
        icon = request.FILES.get('icon')
        # 1. 手动存储
        with open(r'uploads\img\icon.jpg', 'wb') as fp:
            for chunk in icon.chunks():
                fp.write(chunk)
                fp.flush()
        return HttpResponse('upload success')


def image_field(request: HttpRequest):
    if request.method == 'GET':
        return render(request, 'image_field.html')
    elif request.method == 'POST':
        uname = request.POST.get('uname')
        icon = request.FILES.get('icon')

        user = UserModel()
        user.u_name = uname
        user.u_icon = icon
        user.save()

        return HttpResponse(f'user: {user.id} upload success')


def get_icon(request: HttpRequest):
    uname = request.GET.get('uname')

    user = UserModel.objects.get(u_name=uname)
    # print(f'dir: {dir(user.u_icon)}')
    print(f'.url: {user.u_icon.url}')  # 图片 url

    return HttpResponse(f'.url: {user.u_icon.url}')
