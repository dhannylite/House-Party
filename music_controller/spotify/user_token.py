from datetime import timedelta
# from webbrowser import get
# from urllib import response

from .credentials import REDIRECT_URI, CLIENT_ID, CLIENT_SECRET
from turtle import update
from django.utils import timezone
from .models import SpotifyToken
from requests import post, put, get

BASE_URL = "https://api.spotify.com/v1/me/"


def get_user_token(session_id):
    user_token = SpotifyToken.objects.filter(user=session_id)
    if user_token.exists():
        return user_token[0]
    return None


def update_or_create_user_tokens(session_id, access_token, refresh_token, token_type, expires_in):
    tokens = get_user_token(session_id)
    expires_in = timezone.now() + timedelta(seconds=expires_in)

    if tokens:
        tokens.access_token = access_token
        tokens.refresh_token = refresh_token
        tokens.token_type = token_type
        tokens.expires_in = expires_in
        print(tokens.refresh_token, 7777)
        tokens.save(update_fields=['access_token',
                    'refresh_token', 'token_type', 'expires_in'])
    else:
        tokens = SpotifyToken(user=session_id, access_token=access_token,
                              refresh_token=refresh_token, token_type=token_type, expires_in=expires_in)
        tokens.save()


def is_authenticated(session_id):
    tokens = get_user_token(session_id)
    if tokens:
        expiry = tokens.expires_in
        print(expiry)
        if expiry <= timezone.now():
            refresh_token(session_id)
            print('refreshed')
        return True
    return False


def refresh_token(session_id):
    refresh_token = get_user_token(session_id).refresh_token

    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }).json()

    access_token = response.get('access_token')
    refresh_token = refresh_token
    token_type = response.get('token_type')
    expires_in = response.get('expires_in')
    print(response)

    update_or_create_user_tokens(
        session_id, access_token, refresh_token, token_type, expires_in)


def execute_spotify_api_request(session_id, endpoint, post_=False, put_=False):
    token = get_user_token(session_id)
    headers = {"Content-Type": "application/json",
               "Authorization": "Bearer " + token.access_token}

    if post_:
        post(BASE_URL + endpoint, headers=headers)

    if put_:
        put(BASE_URL + endpoint, headers=headers)

    response = get(BASE_URL + endpoint, {}, headers=headers)

    if post_ != True or put_ != True:
        print(response.json(), put_, )

    try:
        return response.json()
    except:
        return {'Error': 'Issue with request'}


def pause_song(session_id):
    return execute_spotify_api_request(session_id, "player/pause", put_=True)


def play_song(session_id):
    return execute_spotify_api_request(session_id, "player/play", put_=True)


def skip_song(session_id):
    return execute_spotify_api_request(session_id, "player/next", post_=True)


def previous_song(session_id):
    # print(session_id)
    return execute_spotify_api_request(session_id, "player/previous", post_=True)


def search_song(session_id, artist, track):
    # print(session_id)
    print(track)
    endpoint = f"https://api.spotify.com/v1/search?q=remaster%2520track%3{track}%2Bartist%3A{artist}&type=track%2Cartist&market=ES&limit=10&offset=5"
    return execute_spotify_api_request(session_id, endpoint)
