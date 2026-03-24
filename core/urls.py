from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from contracts.views import RegisterView, UserDetailView, ContractListCreateView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # JWT Auth Endpoints
    path('api/auth/register/', RegisterView.as_view(), name='auth_register'),
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # User Profile (Verification)
    path('api/auth/me/', UserDetailView.as_view(), name='auth_me'),

    # Contracts Endpoints
    path('api/contracts/', ContractListCreateView.as_view(), name='contract-list-create'),
]