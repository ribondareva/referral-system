import time

from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from .serializers import PhoneSerializer, CodeSerializer, ProfileSerializer, ActivateInviteSerializer
from django.shortcuts import get_object_or_404


_fake_sms_storage = {}


class SendCodeView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=PhoneSerializer)
    def post(self, request):
        serializer = PhoneSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']
        code = '1234'  # всегда одно и то же — имитация
        _fake_sms_storage[phone] = code
        time.sleep(1.5)  # имитация отправки
        return Response({"detail": "Код отправлен"}, status=200)


class VerifyCodeView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=CodeSerializer)
    def post(self, request):
        serializer = CodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']
        code = serializer.validated_data['code']
        if _fake_sms_storage.get(phone) == code:
            user, created = User.objects.get_or_create(phone=phone)
            request.session['phone'] = phone  # примитивная сессия
            return Response({"detail": "Авторизация успешна"})
        return Response({"detail": "Неверный код"}, status=400)


class ProfileView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        phone = request.session.get('phone')
        if not phone:
            return Response({"detail": "Не авторизован"}, status=403)
        user = get_object_or_404(User, phone=phone)
        return Response(ProfileSerializer(user).data)

    @swagger_auto_schema(request_body=ActivateInviteSerializer)
    def post(self, request):
        phone = request.session.get('phone')
        if not phone:
            return Response({"detail": "Не авторизован"}, status=403)
        user = get_object_or_404(User, phone=phone)
        code = request.data.get('code')
        if user.activated_code:
            return Response({"detail": "Код уже активирован"}, status=400)
        referred_user = User.objects.filter(invite_code=code).first()
        if not referred_user:
            return Response({"detail": "Неверный код"}, status=404)
        user.activated_code = referred_user
        user.save()
        return Response({"detail": "Инвайт-код активирован"})
