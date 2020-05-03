from django.conf.urls import url
from app_session import views

urlpatterns = [
    url(r'^index/', views.index, name='index'),
    url(r'^login/', views.login, name='login'),
    url(r'^logged/', views.logged, name='logged'),
    url(r'^logout/', views.logout, name='logout'),

]
