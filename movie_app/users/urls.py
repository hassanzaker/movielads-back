from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('home/', views.home, name='home'),  # Home view for displaying the welcome message
    path('logout/', views.logout, name="logout"),
]
