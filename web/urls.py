from django.urls import path, include
from .api.views import  ProjectViewSet, TagViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('projects', ProjectViewSet, basename='projects')
router.register('tag', TagViewSet, basename='tags')


urlpatterns = [
    path('api/', include(router.urls)),
    # path('projects/', ProjectList.as_view(), name='projects'),
]
