from rest_framework import serializers
from .models import User


class PhoneSerializer(serializers.Serializer):
    phone = serializers.CharField()


class CodeSerializer(serializers.Serializer):
    phone = serializers.CharField()
    code = serializers.CharField()


class ProfileSerializer(serializers.ModelSerializer):
    activated_code = serializers.SerializerMethodField()
    referrals = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['phone', 'invite_code', 'activated_code', 'referrals']

    @staticmethod
    def get_activated_code(obj):
        return obj.activated_code.invite_code if obj.activated_code else None

    @staticmethod
    def get_referrals(obj):
        return [user.phone for user in obj.referrals.all()]


class ActivateInviteSerializer(serializers.Serializer):
    code = serializers.CharField()
