from rest_framework import serializers
from core.models import AppInstalls


class AppInstallsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppInstalls
        fields = '__all__'