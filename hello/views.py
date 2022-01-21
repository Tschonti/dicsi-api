from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
import requests
from rest_framework.response import Response
from django.contrib.postgres.search import SearchQuery

from rest_framework import viewsets

from .serializers import SongSerializer, PlaylistSerializer
from .models import Song, Playlist

from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all().order_by('id')
    serializer_class = SongSerializer

""" class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all().order_by('-created_at')
    serializer_class = PlaylistSerializer """

@api_view(['GET'])
@renderer_classes([JSONRenderer])
def searchTitle(request, term):
    songs = Song.objects.filter(title__search=term)
    return Response(SongSerializer(songs, many=True).data)

@api_view(['GET'])
@renderer_classes([JSONRenderer])
def searchLyrics(request, term):
    songs = Song.objects.filter(lyrics__search=term)
    return Response(SongSerializer(songs, many=True).data)

@api_view(['GET', 'POST'])
@renderer_classes([JSONRenderer])
def playlistIndex(request):
    if request.method == 'GET':
        playlists = Playlist.objects.all()
        return Response(PlaylistSerializer(playlists, many=True).data)
    if request.method == 'POST':
        return

@api_view(['GET', 'POST'])
@renderer_classes([JSONRenderer])
def playlistIndex(request, id):
    if request.method == 'GET':
        playlist = Playlist.objects.get(pk=id)
        return Response(PlaylistSerializer(playlist).data)
    if request.method == 'POST':
        return