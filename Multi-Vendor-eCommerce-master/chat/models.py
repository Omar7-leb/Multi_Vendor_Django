from django.db import models

# Create your models here.

from django.db import models
from customers.models import User
# Create your models here.

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender", default=1)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver", default=1)
    room_name = models.TextField(max_length=100, default="None")
    content = models.TextField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)


    def last_30_messages(selfs):
        return Message.objects.order_by('-timestamp').all()[:30]