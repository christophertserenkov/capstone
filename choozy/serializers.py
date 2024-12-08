from rest_framework import serializers
from .models import Room, Player

# Serializers created by CS50 AI
class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'

class RoomSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True)

    class Meta:
        model = Room
        fields = '__all__'