from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views
from . import views

router = routers.DefaultRouter()
router.register(r'songs', views.SongViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-token-auth/', views.obtain_auth_token),
    path('search/<term>/', views.search)
]