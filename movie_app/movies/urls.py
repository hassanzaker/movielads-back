from django.urls import path
from . import views

urlpatterns = [
    path('movie/<int:id>/', views.get_movie, name='get_movie'),
    path('movies/all/', views.get_all_movies, name='get_all_movies'),
    path('watchlist/add/', views.add_movie_to_watch_list, name="add_movie_to_watch_list"),
    path('seen/add/', views.add_seen_movie, name='add_seen_movie'),
    path('watchlist/', views.get_watchlist, name='get_watchlist'),
    path('seenlist/', views.get_seenlist, name='get_seenlist'),
    path('watchlist/delete/', views.delete_movies_from_watchlist, name="delete_movies_from_watchlist"),
    path('seen/delete/', views.delete_movies_from_seenlist, name="delete_movies_from_seenlist"),
    path('search/movie/', views.search_movie, name="search_movie"),
]
