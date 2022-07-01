from django.urls import path
from .views import AuthURL, CurrentSong, IsAuthenticated, PauseSong, PlaySong, PreviousSong, SearchSong, SkipSong, spotify_callback

urlpatterns = [
    path('get-auth-url', AuthURL.as_view()),
    path('redirect', spotify_callback),
    path('is-authenticated', IsAuthenticated.as_view()),
    path('current-song', CurrentSong.as_view()),
    path('pause', PauseSong.as_view()),
    path('play', PlaySong.as_view()),
    path('skip', SkipSong.as_view()),
    path('previous', PreviousSong.as_view()),
    path('search', SearchSong.as_view())
]