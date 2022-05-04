from django.http import HttpResponse
from rest_framework import status, viewsets, mixins
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from sso.serializers import UserSignUpSerializer, UserBaseSerializer, UserDetailSerializer
from sso.models import User


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSignUpSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def my_profile(request):
    if request.user.id:
        user = User.objects.get(id=request.user.id)
        serializer = UserBaseSerializer(user)
        return Response(serializer.data)
    else:
        return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)


class UserViewSet(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin
):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return User.objects.all()

    def get_serializer_class(self):
        return UserDetailSerializer
