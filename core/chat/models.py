from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):

    receiver = models.ForeignKey(User, related_name="receiver", on_delete=models.CASCADE, null=True)
    sender = models.ForeignKey(User, related_name="sender", on_delete=models.CASCADE, null=True)
    text = models.TextField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    def save(self, sender, text, *args, **kwargs):

        sending_user = User.objects.get(username=sender) if sender != "anonymousUser" else None
        self.sender = sending_user
        self.text = text
        super(self.__class__, self).save(*args, **kwargs)


class Account(models.Model):

    name = models.CharField(max_length=100, null=True)
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    