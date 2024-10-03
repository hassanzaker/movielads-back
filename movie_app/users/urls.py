from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('home/', views.home, name='home'),  # Home view for displaying the welcome message
    path('logout/', views.logout, name="logout"),
]
