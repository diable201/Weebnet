from django.urls import path
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from sso.views import RegistrationAPIView, my_profile, UserViewSet

app_name = 'sso'

router = routers.DefaultRouter()

urlpatterns = [
    path(r'registration/', RegistrationAPIView.as_view()),
    path(r'profile/my/', my_profile),
    path(r'login/', obtain_jwt_token),
    path(r'token-refresh/', refresh_jwt_token),
    path(r'users/', UserViewSet.as_view(
        {
            "get": "list",
        }),
         name="users"
    ),
    path(r'users/<int:pk>/', UserViewSet.as_view(
        {
            "get": "retrieve",
            "put": "update",
            "delete": "destroy"
        }),
        name="users by id"
    )
]

urlpatterns += router.urls
