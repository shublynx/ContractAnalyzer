from rest_framework import serializers
from .models import User, Contract

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
    

class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ['id', 'file', 'name', 'raw_text', 'uploaded_at']
        read_only_fields = ['id', 'raw_text', 'uploaded_at']

    def create(self, validated_data):
        # We automatically assign the logged-in user to the contract
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)