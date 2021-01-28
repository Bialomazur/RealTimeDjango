from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.utils.crypto import get_random_string

def generate_socket_hash():
    return get_random_string(length=32)
    

class Account(models.Model):

    name = models.CharField(max_length=100, null=True)
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    chat_hash = models.TextField(default=generate_socket_hash, max_length=32, unique=True)

    def __str__(self):
        return self.chat_hash


class Message(models.Model):

    receiver = models.ForeignKey(Account, related_name="receiver", on_delete=models.CASCADE, null=True)
    sender = models.ForeignKey(Account, related_name="sender", on_delete=models.CASCADE, null=True)
    text = models.TextField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
 

