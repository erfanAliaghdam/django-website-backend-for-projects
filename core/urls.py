from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api.views import MessageViewSet, CreateTokenViewSet


router = DefaultRouter()
router.register('', MessageViewSet, basename='messages')

routerToken = DefaultRouter()
routerToken.register('create/token', CreateTokenViewSet, basename='create-token')

urlpatterns = [
    path('api/auth/',               include('djoser.urls')),
    path('api/auth/',               include('djoser.urls.jwt')),
    path('api/messages/',           include(router.urls)),
    path('api/auth/',               include(routerToken.urls)),
]
