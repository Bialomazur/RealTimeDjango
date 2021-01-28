from django.shortcuts import render
from chat.models import *
import json

def index(request):
    return render(request, "index.html", {})

def room(request):
    user = request.user
    account = Account.objects.get(user=user)
    contacts = tuple(user.username for user in User.objects.all().exclude(username=user.username))
    print(contacts)

    return render(request, "chatroom.html", {
        "room_name": "room_name",
        "room_hash": account.chat_hash,
        "contacts_json": json.dumps(contacts),
        "contacts": contacts
    })