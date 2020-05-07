from django.conf.urls import url
from app_oneToMany import views

urlpatterns = [
    url(r'^index/', views.index, name='index'),
]
