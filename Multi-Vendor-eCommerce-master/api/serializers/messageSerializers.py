from rest_framework import serializers
from chat.models import Message

class GetRoomSerializer(serializers.ModelSerializer):
    customer = serializers.CharField(read_only=True)
    last_message = serializers.CharField(read_only=True)

    class Meta:
        model = Message
        fields = ["room_name", "customer", "last_message","timestamp"]


class GetMessageSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(source='sender.email')
    receiver = serializers.CharField(source='receiver.email')
    class Meta:
        model = Message
        fields = ["content", "sender", "receiver"]