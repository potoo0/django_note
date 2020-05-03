from django.conf.urls import url
from app_token import views


urlpatterns = [
    url(r'^index/', views.index, name='index'),
    url(r'^register/', views.register, name='register'),
    url(r'^login/', views.login, name='login'),
    url(r'^logged/', views.logged, name='logged'),

]
