from django.conf.urls import url
from app_uploadFiles import views
from django.views.static import serve
from model_migrate_ForeignKey.settings import MEDIA_ROOT

urlpatterns = [
    url(r'^index/', views.index, name='index'),
    url(r'^upload/', views.upload, name='upload'),
    url(r'^imagefield/', views.image_field, name='image_field'),
    url(r'^geticon/', views.get_icon, name='get_icon'),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
]
