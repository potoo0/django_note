from django.conf.urls import url
from app_migrate import views

urlpatterns = [
    url(r'^index/', views.index, name='index'),
]
