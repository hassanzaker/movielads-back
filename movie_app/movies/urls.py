from django.urls import path
from . import views

urlpatterns = [
    path('movie/<int:id>/', views.get_movie, name='get_movie'),
    path('movies/all/', views.get_all_movies, name='get_all_movies'),
    path('watchlist/add/', views.add_movie_to_watch_list, name="add_movie_to_watch_list"),
    path('seen/add/', views.add_seen_movie, name='add_seen_movie')
]
