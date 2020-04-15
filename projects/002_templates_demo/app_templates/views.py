from django.shortcuts import render
from django.http import HttpResponse
# from django.template import loader
from app_templates.models import Student
from datetime import date, datetime


def index(request):
    # template = loader.get_template('app_index.html')
    # content = template.render()
    # return HttpResponse(content)
    return render(request, 'app_index.html')


def createStu(request):
    for index in range(10):
        s = Student(s_name=f'Rick_{index:03}', s_age=15 + index)
        s.save()
    return HttpResponse('create 10 student completely.')


def getStu(request):
    studentsDic = Student.objects.all().values()
    student = Student.objects.first()
    now_date = date.today()
    now_datetime = datetime.now()
    code = '<h5>code</h5><hr><br>'
    return render(request, 'app_stuLis.html', context=locals())


def templateInheritance(request):
    return render(request,
                  'templateInheritance/app_TempChild.html',
                  context={"title": 'child'})
