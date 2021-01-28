from django.contrib import admin
from django.urls import path
from . import views

app_name = "chat"

urlpatterns = [
    path("", views.room, name="room"),
    path("chat/", views.index, name="index")
]