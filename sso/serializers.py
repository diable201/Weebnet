from rest_framework import serializers

from sso.models import User


class UserBaseSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    def validate_password(self, value):
        if value and value < 8:
            raise serializers.ValidationError("Пароль слишком короткий")
        elif value and value > 128:
            raise serializers.ValidationError("Пароль слишком длинный")
        return value

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'date_joined', 'avatar', 'date_of_birth', 'password']


class UserSignUpSerializer(UserBaseSerializer):
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    date_of_birth = serializers.DateTimeField()
