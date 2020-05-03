from django.conf.urls import url
from app_url import views

urlpatterns = [
    url(r'^index/', views.index, name='index'),
    url(r'^hello/', views.hello),
    url(r'^hellooo', views.hellooo),  # wrong
    url(r'^end$', views.hellooo),  # wrong
    url(r'^geturlarg/$', views.hellooo),
    url(r'^geturlarg/(\d+)/', views.geturlarg),
    url(r'^geturlargs_p/(\d+)/(\d+)/',
        views.geturlargs_p, name='geturlargs_p'),
    url(r'^geturlargs_k/(?P<arg1>\d+)/(?P<arg2>\d+)/',
        views.geturlargs_k, name='geturlargs_k'),

]
