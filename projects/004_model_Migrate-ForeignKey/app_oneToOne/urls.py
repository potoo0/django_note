from django.conf.urls import url
from app_oneToOne import views

urlpatterns = [
    url(r'^index/', views.index, name='index'),
    url(r'^addperson/', views.add_person, name='add_person'),
    url(r'^addidcard/', views.add_idcard, name='add_idcard'),
    url(r'^bindidcard/', views.bind_idcard, name='bind_idcard'),
    url(r'^removeperson/', views.remove_person, name='remove_person'),
    url(r'^removeidcard/', views.remove_idcard, name='remove_idcard'),
    url(r'^getpersonbyid/', views.get_person_byid, name='get_person_byid'),
    url(r'^getidbyperson/', views.get_idcard_byperson, name='get_idcard_byperson'),
]
