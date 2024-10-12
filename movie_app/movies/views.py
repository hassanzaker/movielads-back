from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated 
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse

import requests
import json

from django.contrib.auth import get_user_model
from .models import WatchList, SeenList
from .serializers import WatchListSerializer, SeenListSerializer

User = get_user_model()


import tmdbsimple as tmdb
tmdb.API_KEY = 'a246abd7112d8a20850393ee75d04b06'
tmdb.REQUESTS_TIMEOUT = (2, 5)  # seconds, for connect and read specifically 


BASE_URL = "https://api.themoviedb.org/3/"

HEADERS = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJhMjQ2YWJkNzExMmQ4YTIwODUwMzkzZWU3NWQwNGIwNiIsIm5iZiI6MTcyNjkyOTIxNy44ODcxNDEsInN1YiI6IjY2ZWVkODQ3N2ZmMmJmNTdjZDI2MGY5YiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.9V3JBqsEYKZ6fzaJgexPTwtbhmzWxqVY0MFK_T3d99Q"
}

urls = {
    "top_rated": "movie/top_rated",
    "popular": "movie/popular",
    "now_playing": "movie/now_playing",
    "upcoming": "movie/upcoming"

}

@api_view(["GET"])
def get_movie(request, id):
    try:
        movie = tmdb.Movies(id)
        response = movie.info()

        user = request.user
        in_watchlist = False
        is_seen = False
        if user.is_authenticated:
            in_watchlist = WatchList.objects.filter(user=user, movie_id=id).exists()
            is_seen = SeenList.objects.filter(user=user, movie_id=id).exists()

        return Response({"movie": response, "seen": is_seen, "watchlist": in_watchlist}, status=200)
    except Exception as e:
        return Response("Movie Not Found!", status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_all_movies(request):
    list_type = request.query_params.get('list_type')
    page = request.query_params.get('page')

    print(list_type, page)
    if not list_type:
        list_type = "top_rated"

    if list_type in urls:
        url = BASE_URL + urls[list_type]

        params = {
            "language": "en-US",
            "page": page
        }

        response = requests.get(url, headers=HEADERS, params=params)
        content = json.loads(response._content.decode('utf-8'))  # Decode and convert to JSON

        return JsonResponse(content, safe=False, status=200)

    else:
        return Response("URL Not Found!", status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_movie_to_watch_list(request):
    # Extract user_id and movie_id from the request data
    user = request.user
    movie_id = request.data.get('movie_id')
    priority = request.data.get('priority', 2)  # Default priority is Medium
    notes = request.data.get('notes', '')  # Optional notes

    # Validate the presence of user_id and movie_id
    if not movie_id:
        return Response(
            {"error": "'movie_id' is required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Check if the movie exists by calling the get_movie method
    try:
        movie = tmdb.Movies(movie_id)
        response = movie.info()
        movie_title = response['original_title']

    except Exception as e:
        return Response(
            {"error": f"Error fetching movie data: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

        # If everything is fine, add the movie to the user's watchlist
    watchlist_item, created = WatchList.objects.get_or_create(
        user=user,
        movie_id=movie_id,
        defaults={
            'movie_title': movie_title,
            'priority': priority,
            'notes': notes,
        }
    )

    if not created:
        return Response({"message": "Movie already exists in the watchlist."}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"message": "Movie added to watchlist successfully."}, status=status.HTTP_201_CREATED)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_watchlist(request):
    user = request.user

    movies = WatchList.objects.filter(user=user).order_by('added_at')
    # Use the serializer to convert the queryset to JSON
    serializer = WatchListSerializer(movies, many=True)

    return Response(serializer.data, status=200)  # Return the serialized data as JSON


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_seenlist(request):
    user = request.user

    movies = SeenList.objects.filter(user=user).order_by('added_at')
    # Use the serializer to convert the queryset to JSON
    serializer = SeenListSerializer(movies, many=True)

    return Response(serializer.data, status=200)  # Return the serialized data as JSON

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_seen_movie(request):
    # Extract user_id and movie_id from the request data
    user = request.user
    movie_id = request.data.get('movie_id')
    rating = request.data.get('rating')  # Default priority is Medium
    review = request.data.get('review', '')  # Optional notes

    # Validate the presence of user_id and movie_id
    if not movie_id:
        return Response(
            {"error": "'movie_id' is required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Check if the movie exists by calling the get_movie method
    try:
        movie = tmdb.Movies(movie_id)
        response = movie.info()
        movie_title = response['original_title']

    except Exception as e:
        return Response(
            {"error": f"Error fetching movie data: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    exists = WatchList.objects.filter(user=user, movie_id=movie_id).exists()

    if exists:
        notes = WatchList.objects.get(user=user, movie_id=movie_id).notes
        print(notes)
    else:
        notes = ''

        # If everything is fine, add the movie to the user's watchlist
    watchlist_item, created = SeenList.objects.get_or_create(
        user=user,
        movie_id=movie_id,
        defaults={
            'movie_title': movie_title,
            'rating': rating,
            'notes': notes,
            'review': review
        }
    )

    if not created:
        return Response({"message": "You have seen this movie before."}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"message": "Movie added to Seen List successfully."}, status=status.HTTP_201_CREATED)


