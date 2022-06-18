from cgitb import lookup
from django.urls import path, include
from .api.views import  ProjectViewSet, TagViewSet, RequestedItemsViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('projects', ProjectViewSet, basename='projects')
router.register('tag', TagViewSet, basename='tags')
router.register('requested', RequestedItemsViewSet, basename='requested-projects')


registerProjRouter = DefaultRouter()

urlpatterns = [
    path('api/', include(router.urls)),
]
