from django.urls import path, include
from .api.views import  ProjectViewSet, TagViewSet, RequestedItemsViewSet, VerificationViewSet, AcceptRequestsViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('projects', ProjectViewSet, basename='projects')
router.register('tag', TagViewSet, basename='tags')
router.register('requested', RequestedItemsViewSet, basename='requested-projects')
router.register('verification', VerificationViewSet, basename='verification')
router.register('applied', AcceptRequestsViewSet, basename='accept-requests')
registerProjRouter = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
]
