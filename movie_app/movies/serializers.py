from rest_framework import serializers
from rest_framework.response import Response
from .models import WatchList, SeenList


# Define a serializer for the WatchList model
class WatchListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchList
        fields = ['movie_id', 'movie_title', 'priority', 'notes', 'added_at']


class SeenListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeenList
        fields = ['movie_id', 'movie_title', 'rating', 'notes', 'added_at', 'review']

