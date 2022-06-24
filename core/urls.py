from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api.views import MessageViewSet


router = DefaultRouter()
router.register('', MessageViewSet, basename='messages')

urlpatterns = [
    path('api/auth/',               include('djoser.urls')),
    path('api/auth/',               include('djoser.urls.jwt')),
    path('api/messages/',           include(router.urls)),
]
