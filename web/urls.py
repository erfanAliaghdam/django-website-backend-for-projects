from django.urls import path, include
from .api.views import  ProjectViewSet, TagViewSet, RequestedItemsViewSet, VerificationViewSet, AcceptRequestsViewSet, MentorMessageViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('projects', ProjectViewSet, basename='projects')
router.register('tag', TagViewSet, basename='tags')
router.register('request', RequestedItemsViewSet, basename='requested-projects')
router.register('verification', VerificationViewSet, basename='verification')
router.register('apply', AcceptRequestsViewSet, basename='accept-requests')
router.register('admission/messages', MentorMessageViewSet, basename='admission-messages')


urlpatterns = [
    path('', include(router.urls)),
]
