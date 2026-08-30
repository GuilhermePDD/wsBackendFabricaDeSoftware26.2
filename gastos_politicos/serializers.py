from rest_framework import serializers

from .models import Governador, Gasto


class GovernadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Governador
        fields = "__all__"


class GastoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gasto
        fields = "__all__"
