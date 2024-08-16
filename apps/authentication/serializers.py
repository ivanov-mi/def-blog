from rest_framework import serializers
from .models import CustomUser
from rest_framework.authtoken.models import Token


class LoginUserSerializer(serializers.ModelSerializer):

    username = serializers.CharField(read_only=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password']


class CreateUserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        Token.objects.create(user=user)

        return user
