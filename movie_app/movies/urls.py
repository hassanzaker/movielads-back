from django.urls import path
from . import views

urlpatterns = [
    path('movie/<int:id>/', views.get_movie, name='get_movie'),
    path('all/', views.get_all_movies, name='get_all_movies'),
]