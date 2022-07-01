import code
from email.mime import image
from os import access
# from urllib import response
# from urllib import response
from django.shortcuts import redirect, render
from rest_framework.views import APIView

from .models import Votes
from .user_token import *
from .credentials import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
from requests import post, Request
from rest_framework import status
from rest_framework.response import Response
from api.models import Room

class AuthURL(APIView):
    def get(self, request, format=None):
        scopes = 'user-read-playback-state user-modify-playback-state user-read-currently-playing'
        url = Request('GET', 'https://accounts.spotify.com/authorize', params={
            'scope':scopes,
            'response_type': 'code',
            'client_id': CLIENT_ID,
            'redirect_uri': REDIRECT_URI
        }).prepare().url
        return Response({"url":url}, status=status.HTTP_200_OK)

def spotify_callback(request, format=None):
    # print(5)
    code = request.GET.get('code')
    error = request.GET.get('error')

    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }).json()

    access_token = response.get('access_token')
    refresh_token = response.get('refresh_token')
    token_type = response.get('token_type')
    expires_in = response.get('expires_in')
    error = response.get('error')

    if not request.session.exists(request.session.session_key):
        request.session.create()
    # print(response)
    update_or_create_user_tokens(request.session.session_key, access_token, refresh_token, token_type, expires_in)

    return redirect('index')

class IsAuthenticated(APIView):
    def get(self, request, format=None):
        authenticated = is_authenticated(self.request.session.session_key)
        # print(authenticated)
        return Response({"status":authenticated}, status=status.HTTP_200_OK)

class CurrentSong(APIView):
    def get(self, request, format=None):
        room_code = self.request.session.get('room_code')
        room = Room.objects.filter(code=room_code)
        if room.exists():
            room = room[0]
        else:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        host = room.host
        endpoint = "player/currently-playing"
        response = execute_spotify_api_request(host, endpoint)
        
        item = response.get('item')
        duration = item.get('duration_ms')
        progress = response.get('progress_ms')
        album_cover = item.get('album').get('images')[0].get('url')
        is_playing = response.get('is_playing')
        song_id = item.get('id')
        artist_str = ''


        for i, artist in enumerate(item.get('artists')):
            if i > 0:
                artist_str += ', '
            name = artist.get('name')
            artist_str += name
        votes = len(Votes.objects.filter(room=room, song_id=song_id))
        print('votes', votes)
        song = {
            'title': item.get('name'),
            'image_url': album_cover,
            'duration': duration,
            'is_playing': is_playing,
            'id': song_id,
            'time': progress,
            'votes': votes,
            'votes_required': room.vote_to_skip,
            'artists': artist_str
        }
        # print(room.code)
        self.update_room_song(room, song_id)
        return Response(song, status=status.HTTP_200_OK)

    def update_room_song(self, room, song_id):
        # print(room.code)
        current_song = room.current_song

        if current_song != song_id:
            room.current_song = song_id
            room.save(update_fields=["current_song"])
            votes = Votes.objects.filter(room=room)
            print(room.current_song)
            votes.delete()


class PauseSong(APIView):
    def put(self, request, format=None):
        room_code = self.request.session.get('room_code')
        room = Room.objects.filter(code=room_code)
        room = room[0]
        if self.request.session.session_key == room.host or room.guest_can_pause:
            pause_song(room.host)
            return Response({}, status=status.HTTP_200_OK)
        return Response({"":""}, status=status.HTTP_403_FORBIDDEN)

class PlaySong(APIView):
    def put(self, request, format=None):
        room_code = self.request.session.get('room_code')
        room = Room.objects.filter(code=room_code)
        room = room[0]
        if self.request.session.session_key == room.host or room.guest_can_pause:
            play_song(room.host)
            return Response({}, status=status.HTTP_200_OK)
        return Response({"":""}, status=status.HTTP_403_FORBIDDEN)

class SkipSong(APIView):
    def post(self, request, format=None):
        room_code = self.request.session.get('room_code')
        room = Room.objects.filter(code=room_code)
        room = room[0]
        votes = Votes.objects.filter(room=room, song_id=room.current_song)
        votes_needed = room.vote_to_skip
        if self.request.session.session_key == room.host or len(votes) + 1 >= votes_needed:
            votes.delete()
            skip_song(room.host)
        else:
            vote = Votes(user=self.request.session.session_key, room=room, song_id=room.current_song)
            print(len(votes), 67775, votes_needed, vote, votes)
            vote.save()

        return Response({"":""}, status=status.HTTP_204_NO_CONTENT)

class PreviousSong(APIView):
    def post(self, request, format=None):
        room_code = self.request.session.get('room_code')
        room = Room.objects.filter(code=room_code)
        room = room[0]
        if self.request.session.session_key == room.host:
            print('previous')
            previous_song(room.host)
            return Response({}, status=status.HTTP_200_OK)
        return Response({"":""}, status=status.HTTP_403_FORBIDDEN)

class SearchSong(APIView):
    def get(self, request, format=None):
        room_code = self.request.session.get('room_code')
        room = Room.objects.filter(code=room_code)
        room = room[0]
        # artist = self.request.get.data('artist')
        # track = self.request.get.data('track')
        artist = "dua lipa"
        track = "levitating"
        if self.request.session.session_key == room.host:
            search_song(room.host, artist, track)
            return Response({}, status=status.HTTP_200_OK)
        return Response({"":""}, status=status.HTTP_403_FORBIDDEN)

