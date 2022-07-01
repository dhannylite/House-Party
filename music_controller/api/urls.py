from django.urls import path
from .views import CreateRoomView, GetRoomView, JoinRoom, LeaveRoom, RoomView, UpdateRoom, userInRoom

urlpatterns = [
    path('room', RoomView.as_view()),
    path('create', CreateRoomView.as_view()),
    path('get-room', GetRoomView.as_view()),
    path('join-room', JoinRoom.as_view()),
    path('user-in-room', userInRoom.as_view()),
    path('leave-room', LeaveRoom.as_view()),
    path('update-room', UpdateRoom.as_view()),
]
