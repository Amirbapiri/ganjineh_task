from rest_framework.serializers import ModelSerializer

from core_apps.tokens.models import Token, TokenPrice


class TokenSerializer(ModelSerializer):
    class Meta:
        model = Token
        fields = "__all__"


class TokenPriceSerializer(ModelSerializer):
    class Meta:
        model = TokenPrice
        fields = "__all__"
