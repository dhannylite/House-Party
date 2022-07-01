import code
import re
from django.shortcuts import render
from rest_framework import generics
from .serializers import CreateRoomSerializer, RoomSerializer, UpdateRoomSerializer
from .models import Room
from rest_framework.views import APIView, status
from rest_framework.response import Response
from django.http import JsonResponse


# Create your views here.

class RoomView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class CreateRoomView(APIView):
    serializer_class = CreateRoomSerializer

    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        serializer = CreateRoomSerializer(data=request.data)
        # print(serializer)
        if serializer.is_valid():
            guest_can_pause = serializer.data.get('guest_can_pause')
            vote_to_skip = serializer.data.get('vote_to_skip')
            host = self.request.session.session_key
            queryset = Room.objects.filter(host=host)
            if queryset.exists():
                room = queryset[0]
                room.guest_can_pause = guest_can_pause
                room.vote_to_skip = vote_to_skip
                self.request.session['room_code'] = room.code
                room.save(update_fields=['guest_can_pause', 'vote_to_skip'])
            else:
                room = Room(host=host, guest_can_pause=guest_can_pause, vote_to_skip=vote_to_skip)
                room.save()
                self.request.session['room_code'] = room.code
            return Response(RoomSerializer(room).data, status=status.HTTP_201_CREATED)

class GetRoomView(APIView):
    serializer_class = RoomSerializer
    lookup_url_kwarg = 'code'
    
    def get(self, request, format=None):
        code = request.GET.get(self.lookup_url_kwarg)
        # print(code)
        if code:
            room = Room.objects.filter(code=code)
            if len(room) > 0:
                data = RoomSerializer(room[0]).data
                data['is_Host'] = self.request.session.session_key == room[0].host
                # print(data)
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({'Room Not Found': 'Invalid code'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'Bad Request': 'Code Parameter not found'}, status=status.HTTP_400_BAD_REQUEST)

class JoinRoom(APIView):
    lookup_url_kwarg = 'code'

    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        code = request.data.get(self.lookup_url_kwarg)
        if code:
            room_result = Room.objects.filter(code=code)
            if len(room_result) > 0:
                room = room_result[0]
                self.request.session['room_code'] = code
                return Response({'message':'Room Joined'}, status=status.HTTP_200_OK)
            return Response({'Bad Request':'Invalid Room Code'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'Bad Request':'Invalid Post Data'}, status=status.HTTP_400_BAD_REQUEST)


class userInRoom(APIView):
    def get(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        data = {
            'code': self.request.session.get('room_code')
        }
        print(data)

        return JsonResponse(data, status=status.HTTP_200_OK)


class LeaveRoom(APIView):
    def post(self, request, format=None):
        request.session.pop('room_code')
        host_id = request.session.session_key
        room_result = Room.objects.filter(host=host_id)
        if room_result:
            room = room_result[0]
            room.delete()
        return Response({"Message": "success"}, status=status.HTTP_200_OK)

class UpdateRoom(APIView):
    def patch(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        serializer = UpdateRoomSerializer(data=request.data)
        if serializer.is_valid():
            guest_can_pause = serializer.data.get('guest_can_pause')
            vote_to_skip = serializer.data.get('vote_to_skip')
            code = serializer.data.get('code')
            queryset = Room.objects.filter(code=code)
            print(queryset)
            if not queryset.exists():
                return Response({'message': 'Could not find room'}, status=status.HTTP_404_NOT_FOUND)
            room = queryset[0]
            user_id = self.request.session.session_key
            if user_id != room.host:
                return Response({'Forbidden': 'You are not the host'}, status=status.HTTP_403_FORBIDDEN)
                
            room.guest_can_pause = guest_can_pause
            room.vote_to_skip = vote_to_skip    
            room.save(update_fields=['guest_can_pause', 'vote_to_skip'])
            return Response({'message': 'successful'}, status=status.HTTP_200_OK)

        return Response({'Bad Request': 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)


