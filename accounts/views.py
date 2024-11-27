from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import AllowAny
from .serializers import UserRegistrationSerializer

# Create your views here.


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return Response(
                {"detail": "Successfully logged in.", "username": user.username},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED
            )


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response(
            {"detail": "Successfully logged out."}, status=status.HTTP_200_OK
        )


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            return Response(
                {
                    "detail": "Successfully registered and logged in.",
                    "username": user.username,
                    "email": user.email,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
