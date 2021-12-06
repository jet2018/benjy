from rest_framework import serializers

from .models import UsageData


class UsageDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsageData
        fields = '__all__'
