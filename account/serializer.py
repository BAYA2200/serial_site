from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password, ])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise ValidationError('Password do not match')
        return data

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
# class LoginSerializer(serializers.ModelSerializer):  # Изменил базовый класс
#     password = serializers.CharField(write_only=True)
#
#     class Meta:
#         model = User
#         fields = ('username', 'password')  # Убрал 'email' поле, так как его нет в модели User
#
#     def validate(self, data):
#         username = data.get('username')
#         password = data.get('password')
#
#         if username and password:
#             user = authenticate(username=username, password=password)
#             if not user or not user.is_active:
#                 raise serializers.ValidationError('Unable to log in with provided credentials.')
#         else:
#             raise serializers.ValidationError('Must include "username" and "password".')
#
#         data['user'] = user
#         return data



