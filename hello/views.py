from django.shortcuts import render
from django.http import HttpResponse
import requests

from rest_framework import viewsets

from .serializers import SongSerializer
from .models import Song

class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all().order_by('id')
    serializer_class = SongSerializer

# Create your views here.
def index(request):
    r = requests.get('http://httpbin.org/status/418')
    print(r.text)
    return HttpResponse('<pre>' + r.text + '</pre>')


