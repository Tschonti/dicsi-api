from django.contrib import admin
from .models import Song

#class SongInPlaylistInline(admin.TabularInline):
#    model = SongInPlaylist
#    extra = 1
#
#class SongAdmin(admin.ModelAdmin):
#    inlines = (SongInPlaylistInline,)
#
#class PlaylistAdmin(admin.ModelAdmin):
#    inlines = (SongInPlaylistInline,)

admin.site.register(Song)
#admin.site.register(Playlist, PlaylistAdmin)
