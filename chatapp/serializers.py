from rest_framework import serializers

from chatapp.models import Thread, Message


class ThreadCreateDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = ['participant1', 'participant2', 'created', 'updated']
        read_only_fields = ['created', 'updated']


class ThreadListSerializer(serializers.Serializer):
    participant1 = serializers.CharField(max_length=250, read_only=True)
    participant2 = serializers.CharField(max_length=250, read_only=True)
    last_message_text = serializers.CharField(read_only=True)
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)


class MessageListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['sender', 'text', 'thread', 'created', 'is_read']
        read_only_fields = ['created', 'is_read']


class IsReadUpdateSerializer(serializers.Serializer):
    is_read_ids = serializers.JSONField()
