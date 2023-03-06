from django.contrib.auth.models import User
from django.db.models import Q, F
from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.views import APIView

from chatapp.mixins import thread_exists, correct_users, correct_sequence, correct_user_ids
from chatapp.models import Thread, Message
from chatapp.serializers import ThreadCreateDestroySerializer, ThreadListSerializer, MessageListCreateSerializer, \
    IsReadUpdateSerializer
from django.db.models import Subquery, OuterRef


class ThreadCreateDestroyAPIView(GenericAPIView,
                                 CreateModelMixin,
                                 ):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ThreadCreateDestroySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        thread = thread_exists(serializer=serializer)

        # Check if thread relation exists
        if thread:
            serializer = self.get_serializer(thread)
            return Response(serializer.data, status=HTTP_200_OK)

        # If sender id != participants id and user exists in User
        parts = [serializer.data['participant1'], serializer.data['participant2']]
        user_ids = list(User.objects.values_list('id', flat=True))

        if correct_users(serializer=serializer):
            if correct_user_ids(parts, user_ids):
                return self.create(request)

        return Response({'message': 'Incorrect participants.'},
                        status=HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        id1, id2 = correct_sequence(serializer=serializer)
        obj = Thread.objects.create(participant1=id1, participant2=id2)
        obj.save()
        headers = self.get_success_headers(serializer.data)
        return Response({'created': serializer.data}, status=status.HTTP_201_CREATED, headers=headers)

    def delete(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        thread = thread_exists(serializer=serializer)

        if thread:
            thread.delete()

            return Response({'deleted': serializer.data}, status=HTTP_200_OK)
        return Response({'message': 'Nothing to delete'}, status=HTTP_400_BAD_REQUEST)


class ThreadListAPIView(GenericAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = ThreadListSerializer

    def get_queryset(self):
        last_message = Message.objects.filter(
            thread_id=OuterRef('pk')
        ).order_by('-created').values('text', 'sender_id')[:1]

        try:
            threads = Thread.objects.filter(
                Q(participant1=self.kwargs['pk']) | Q(participant2=self.kwargs['pk'])
            ).annotate(
                last_message_text=Subquery(last_message.values('text')),
                last_message_sender=Subquery(last_message.values('sender_id'))
            ).values(
                'participant1',
                'participant2',
                'created',
                'updated',
                'last_message_text',
                'last_message_sender'
            ).order_by()
        except KeyError:
            return
        return threads

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(self.queryset)


class MessageListCreateAPIView(GenericAPIView,
                               CreateModelMixin,
                               ):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MessageListCreateSerializer

    def get_queryset(self):
        try:
            thread = Thread.objects.get(id=self.kwargs['pk'])
            messages = Message.objects.filter(thread=thread)
        except KeyError:
            return
        return messages

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(self.queryset)

    def post(self, request, *args, **kwargs):
        return self.create(request)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        thread_ids = Thread.objects.filter(participant1=serializer.data['sender']) | Thread.objects.filter(
            participant2=serializer.data['sender'])
        result_thread = thread_ids.values_list('id', flat=True)

        if serializer.data['sender'] in User.objects.values_list('id', flat=True) and \
                serializer.data['thread'] in result_thread:
            sender = User.objects.get(id=serializer.data['sender'])
            thread = Thread.objects.get(id=serializer.data['thread'])
            obj = Message.objects.create(sender=sender,
                                         text=serializer.data['text'],
                                         thread=thread)
            obj.save()
            headers = self.get_success_headers(serializer.data)
            return Response({'created': serializer.data}, status=status.HTTP_201_CREATED, headers=headers)
        return Response({'message': 'Incorrect data'}, status=status.HTTP_400_BAD_REQUEST)


class IsReadUpdateAPIView(GenericAPIView,
                          ListModelMixin):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = IsReadUpdateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        ids = set(serializer.data['is_read_ids'])
        messages = set(Message.objects.values_list('id', flat=True))

        if ids.issubset(messages) or messages.issubset(ids):
            Message.objects.filter(id__in=ids).update(is_read=1)
            return Response({'is_read_True': serializer.data})
        return Response({'message': 'Incorrect data'}, status=status.HTTP_400_BAD_REQUEST)


class IsNotReadAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        try:
            count = Message.objects.filter(
                Q(thread__participant1=self.kwargs['pk']) & ~Q(sender_id=F('thread__participant1')) |
                Q(thread__participant2=self.kwargs['pk']) & ~Q(sender_id=F('thread__participant2')),
                is_read=False
            ).count()
        except KeyError:
            return
        return count

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        return Response({'total_not_read_messages': queryset})
