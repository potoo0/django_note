from django.conf.urls import url
from app_templates import views


urlpatterns = [
    url(r'^index/', views.index),
    url(r'createStu/', views.createStu),
    url(r'getStu/', views.getStu),
    url(r'tempInher/', views.templateInheritance),
]
