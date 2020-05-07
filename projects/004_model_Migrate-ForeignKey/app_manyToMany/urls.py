from django.conf.urls import url
from app_manyToMany import views

urlpatterns = [
    url(r'^index/', views.index, name='index'),
]
