from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout, name="logout"),
    path('profile/', views.get_profile, name="get_profile"),
    path('profile/update/', views.update_profile, name="update_profile"),
]
