from rest_framework import serializers
from .models import Room


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
        extra_kwargs = {
            'hotel': {'required': False}
        }