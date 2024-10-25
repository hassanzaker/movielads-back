from django.urls import path
from . import views

urlpatterns = [
    path('start/', views.start_game, name='start_game'),
    path('question/', views.get_question, name='get_question'),
    path('answer/', views.submit_answer, name='submit_answer'),
    path('status/', views.get_game_status, name='get_game_status'),
]
