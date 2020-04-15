from django.shortcuts import render
# from django.http import HttpResponse
from app_model.models import Grade, Student, dateDemo
# from django.core.exceptions import MultipleObjectsReturned


# Create your views here.
def index(request):
    return render(request, 'index.html')


def createDate(request):
    # 1. 关联表插入数据
    for index in range(1, 3):
        g = Grade.objects.create(g_name=f'g_{index:03}')
        g.save()

    # 2.1 简单插入：先实例化再赋值。
    s1 = Student()
    s1.s_name = 'Rick_001'
    s1.s_grade_id = 1
    s1.save()

    # 2.2 实例化时传入关键字参数
    s2 = Student(s_name='Rick_002', s_grade_id=2)
    s2.save()

    # 2.3 模型管理器的 create 方法，传入关键字参数
    s3 = Student.objects.create(s_name='Rick_003', s_grade_id=1)
    s3.save()

    # 2.3在创建对象时未指定 s_grade_id，会引发不能为空的错误
    s4 = Student.objects.create(s_name='Rick_004', s_age=18)
    s4.save()
