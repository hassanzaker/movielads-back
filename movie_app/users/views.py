from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated 
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import authenticate, login, logout as auth_logout
from .serializers import UserSerializer
from .models import CustomUser
from .forms import CustomUserCreationForm



@csrf_exempt
@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return Response({"message": "User created successfully!"}, status=status.HTTP_201_CREATED)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
def signin(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)

    if user:
        # Log in the user (for session management if needed)
        login(request, user)

        # Create JWT token
        refresh = RefreshToken.for_user(user)

        # Get the avatar URL
        avatar_url = None
        if user.avatar:
            avatar_url = user.avatar.url  # This will provide the URL to the avatar image

        # Return the token and user info, including the avatar URL
        return Response({
            "message": "Login Successful",
            "refresh": str(refresh),
            "token": str(refresh.access_token),
            "user": {
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "avatar": avatar_url,  # Return the URL of the avatar
            }
        }, status=status.HTTP_200_OK)

    return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def logout(request):
    auth_logout(request)  # Log out the current user
    return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def home(request):
    if request.method == 'GET':
        user = request.user
        return Response({"message": f"Welcome, {user.username}"}, status=200)
