from django.conf.urls import url
from app_cookie import views

urlpatterns = [
    url(r'^response_/', views.response_),
    url(r'^respRedirect/', views.respRedirect),
    url(r'^getjson/', views.getjson),
    url(r'^setcookie/', views.setcookie),
    url(r'^getcookie/', views.getcookie),
    url(r'^login/', views.login, name='login'),
    url(r'^dologin/', views.do_login, name='do_login'),
    url(r'^logged/', views.logged, name='logged'),
    url(r'^logout/', views.logout, name='logout'),

]
