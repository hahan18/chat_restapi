from django.contrib.auth.models import User
from django.db import models


class Thread(models.Model):
    # 2 fields participant1, participant2 instead of 1 participants field
    participant1 = models.IntegerField()
    participant2 = models.IntegerField()
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Thread'
        verbose_name_plural = 'Threads'
        ordering = ['updated']

    def __str__(self):
        return str(self.id)


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.PROTECT)
    text = models.TextField()
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='thread_point')
    created = models.DateTimeField(auto_now=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id) + str(self.sender)

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ['created', 'is_read']
