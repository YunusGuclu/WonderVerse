from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name='index'),
    path('uzay/', views.uzay_sayfasi, name='uzay'),
    path('hayvanlar/', views.hayvanlar_sayfasi, name='hayvanlar'),
    path('oyunlar/', views.oyun_eglence_sayfasi, name='oyunlar'),
    path('kesif/', views.kesif_sanat_sayfasi, name='kesif'),
    path('mutfak/', views.mutfak_sayfasi, name='mutfak'),
    path('mutfak/<int:id>/', views.mutfak_detay, name='mutfak_detay'),
]