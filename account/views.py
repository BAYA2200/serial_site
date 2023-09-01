from rest_framework.authtoken.models import Token

from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from account.models import User
from account.serializer import LoginSerializer, RegisterSerializer


class RegisterView(CreateAPIView):
    """
    Blog API endpoint to get list of blogs and create blogs
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def get(self, request):
        return render(request, 'register.html')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
            return redirect('login')  # Перенаправление на главную страницу сайта
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     try:
    #         self.perform_create(serializer)
    #     except ValueError as e:
    #         return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    #     else:
    #         headers = self.get_success_headers(serializer.data)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class LoginView(APIView):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():  # Проверяем, что сериализатор прошел валидацию
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                return redirect('tvshow_list')  # Перенаправление на главную страницу после успешного входа
            else:
                return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # def post(self, request):
    #     serializer = LoginSerializer(data=request.data)
    #
    #     if serializer.is_valid():  # Проверяем, что сериализатор прошел валидацию
    #         username = serializer.validated_data['username']
    #         password = serializer.validated_data['password']
    #         user = authenticate(username=username, password=password)
    #
    #         if user is not None:
    #             login(request, user)
    #             token, created = Token.objects.get_or_create(user=user)
    #             return Response({'token': token.key}, status=status.HTTP_200_OK)
    #
    #         # Ваш код для аутентификации пользователя
    #
    #         return Response({'message': 'Successfully logged in'}, status=status.HTTP_200_OK)
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):

    def post(self, request):
        logout(request)
        return Response({'message': 'User logged out successfully'}, status=status.HTTP_200_OK)

