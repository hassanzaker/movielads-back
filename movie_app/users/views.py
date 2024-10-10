from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from django.views.decorators.csrf import ensure_csrf_cookie

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated 
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import authenticate, login, logout as auth_logout
from .serializers import UserSerializer
from .models import CustomUser
from .forms import CustomUserCreationForm



@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return Response({"message": "User created successfully!"}, status=status.HTTP_201_CREATED)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)



# @ensure_csrf_cookie
@api_view(['POST'])
def signin(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)

    if user:
        login(request, user)
        avatar_url = user.avatar.url if user.avatar else None

        # Get or set the CSRF token
        response = Response({
            "message": "Login Successful",
            "user": {
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "avatar": avatar_url,
            }
        }, status=status.HTTP_200_OK)

        # Include the CSRF token in the response cookies
        # response.set_cookie('csrftoken', csrf_token, httponly=True, samesite='None', secure=True)

        return response

    return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def logout(request):
    auth_logout(request)
    response = Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
    response.delete_cookie('csrftoken')
    response.delete_cookie('sessionid')
    return response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def home(request):
    user = request.user
    return Response({"message": f"Welcome, {user.username}"}, status=200)

