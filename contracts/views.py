from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSerializer
from .models import User

class RegisterView(generics.CreateAPIView):
    """
    Standard 'Public' endpoint for creating a new Lead Engineer account.
    """
    queryset = User.objects.all()
    permission_classes = (AllowAny,) # Anyone can register
    serializer_class = UserSerializer

class UserDetailView(generics.RetrieveAPIView):
    """
    Protected endpoint to verify the JWT is working.
    """
    permission_classes = (IsAuthenticated,) # ONLY logged-in users
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user