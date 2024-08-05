from .models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from config.settings.base import V1_PROMPTS, V2_PROMPTS
from core.models import Prompts

import os


class RegisterView(APIView):
    def __register_prompts(self, user):
        for prompts in [V1_PROMPTS, V2_PROMPTS]:
            for prompt in prompts:
                with open(prompt, "r") as f:
                    text = f.read()
                filename = os.path.basename(prompt)
                filename = os.path.splitext(filename)[0]

                Prompts.objects.create(user=user, text=text, name=filename).save()

    def post(self, request, *args, **kwargs):
        password = request.data.get("password")
        username = request.data.get("username")
        if not password or not username:
            return Response(
                {"error": "Please provide username, password"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST
            )
        user = User.objects.create_user(username=username, password=password)
        self.__register_prompts(user)
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        )


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = User.objects.filter(username=username).first()
        if user is None or not user.check_password(password):
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
            )
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        )
