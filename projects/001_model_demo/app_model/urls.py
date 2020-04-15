from django.conf.urls import url
from app_model import views

urlpatterns = [
    url(r'^index/', views.index),
]
