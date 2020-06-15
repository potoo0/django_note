from django.conf.urls import url
from app_cache import views


urlpatterns = [
    url(r'^index/', views.index, name='index'),
    url(r'^cachedemo/', views.cachedemo, name='cachedemo'),
]
