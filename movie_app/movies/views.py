from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated 
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse

import requests
import json



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
        return Response({"movie": response}, status=200)
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

