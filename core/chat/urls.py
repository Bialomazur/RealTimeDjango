from django.contrib import admin
from django.urls import path
from . import views

app_name = "chat"

urlpatterns = [
    path("chat/room/<str:room_name>/", views.room, name="room"),
    path("chat/", views.index, name="index")
]