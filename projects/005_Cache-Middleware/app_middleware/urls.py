from django.conf.urls import url
from app_middleware import views


urlpatterns = [
    url(r'^index/', views.index, name='index'),
    url(r'^testaop1/', views.testaop1, name='testaop1'),
    url(r'^testaop2/', views.testaop2, name='testaop2'),
]
