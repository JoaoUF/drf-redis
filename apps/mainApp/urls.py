from django.urls import path
from apps.mainApp import views

urlpatterns = [
    path('musician/', views.MusicianList.as_view()),
    path('musician/<uuid:pk>/', views.MusicianDetail.as_view()),
    path('album/', views.AlbumList.as_view()),
    path('album/<uuid:pk>/', views.AlbumDetail.as_view()),
]