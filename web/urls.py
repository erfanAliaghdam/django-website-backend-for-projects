from django.urls import path, include
from .api.views import  ProjectViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', ProjectViewSet, basename='projects')




urlpatterns = [
    path('projects/api/', include(router.urls)),
    # path('projects/', ProjectList.as_view(), name='projects'),
]
