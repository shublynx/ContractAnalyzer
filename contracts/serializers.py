from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    # We write-only the password so it never leaks in an API response
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password')

    def create(self, validated_data):
        # Use create_user to handle password hashing automatically
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user