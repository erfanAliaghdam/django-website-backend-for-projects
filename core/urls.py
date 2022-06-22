from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api.views import MessageViewSet


router = DefaultRouter()
router.register('', MessageViewSet, basename='messages')

urlpatterns = [
    path('',                    include('djoser.urls')),
    path('auth/',               include('djoser.urls.jwt')),
    path('messages/',           include(router.urls)),
]
