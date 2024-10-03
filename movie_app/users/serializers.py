from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'birth_date', 'favorite_movie', 'password']
        extra_kwargs = {
            'password': {'write_only': True}  # Make sure password is write-only
        }

    def create(self, validated_data):
        # Override the create method to handle password hashing
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)  # Hash the password before saving
        user.save()
