from rest_framework import serializers
from chat.models import Message

class GetRoomSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(source='sender.email')
    receiver = serializers.CharField(source='receiver.email')

    class Meta:
        model = Message
        fields = ["room_name", "sender", "receiver"]


class GetMessageSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(source='sender.email')
    receiver = serializers.CharField(source='receiver.email')
    class Meta:
        model = Message
        fields = ["content", "sender", "receiver"]