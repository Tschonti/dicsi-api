from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, JsonResponse
import requests
import json
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
        print('post')
        try:
            req = json.loads(request.body)
            print(req)
            if req["name"]:
                print('van name')
                newPlaylist = Playlist(name=req["name"])
                newPlaylist.save()
                if req["songs"]:
                    print('van songs')
                    if type(req["songs"]) != list:
                        print('de nem lista')
                        raise json.JSONDecodeError('this isn\'t a list', req["songs"], 1)
                    songsToAdd = Song.objects.filter(pk__in=req["songs"])
                    newPlaylist.songs.add(*songsToAdd)
                print('sikerült')
                return Response(PlaylistSerializer(newPlaylist).data)
            else:
                print('nincs name')
                raise json.JSONDecodeError('name field is required', req["name"], 1)
        except json.JSONDecodeError:
            print('bad request')
            return HttpResponseBadRequest()

@api_view(['GET', 'PUT', 'DELETE'])
@renderer_classes([JSONRenderer])
def playlistSingular(request, id):
    try:
        playlist = Playlist.objects.get(pk=id)
        if request.method == 'GET':
            return Response(PlaylistSerializer(playlist).data)
        if request.method == 'PUT':
            if request.POST.get("name"):
                playlist.name = request.POST.get("name")
                playlist.save()
                playlist.songs.clear()
                if request.POST.get("songs"):
                    try:
                        songList = json.loads(request.POST.get("songs"))
                        if type(songList) != list:
                            raise json.JSONDecodeError('this isn\'t a list', request.POST.get("songs"), 1)
                        songsToAdd = Song.objects.filter(pk__in=songList)
                        playlist.songs.add(*songsToAdd)
                    except json.JSONDecodeError:
                        return HttpResponseBadRequest()
                return Response(PlaylistSerializer(playlist).data)
            else:
                return HttpResponseBadRequest()
        if request.method == 'DELETE':
            playlist.delete()
            return Response(status=200)
    except Playlist.DoesNotExist:
        return HttpResponseNotFound() 