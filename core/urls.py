from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api.views import MessageViewSet, CreateTokenViewSet


router = DefaultRouter()
router.register('', MessageViewSet, basename='messages')

routerToken = DefaultRouter()
routerToken.register('', CreateTokenViewSet, basename='create')

urlpatterns = [
    path('api/auth/',               include('djoser.urls')),
    path('api/auth/',               include('djoser.urls.jwt')),
    path('api/messages/',           include(router.urls)),
    path('api/auth/create/token/',  include(routerToken.urls)),
]
