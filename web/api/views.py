from multiprocessing import context
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.db.models import Count
from django.conf import settings
from .serializers import (ProjectSerializer, TagSerializer, RequestedItemsSerializer, VerificationDocSerializer)
from ..models import Project, Tag, RequestItem, VerificationDoc
from ..permissions import IsAdminOrReadOnly, IsMentorOrReadOnly

# Create your views here.




class ProjectViewSet(ModelViewSet):
    queryset           = Project.objects.prefetch_related('tag').all().annotate(
        num_tags=Count('tag')
    )
    serializer_class   = ProjectSerializer
    filter_backends    = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    filterset_fields   = ['tag']
    search_fields      = ['title', 'description']
    ordering_fields    = ['num_tags']    
    permission_classes = [IsMentorOrReadOnly]

    def num_tags(self, obj):
        return obj.num_tags
    


    # @action(detail=True, methods=['post'], url_path='request', permission_classes=[IsAuthenticated])
    # def request_project(self, request, *args, **kwargs):
    #     project = self.get_object()
    #     print(project)

class TagViewSet(ReadOnlyModelViewSet):
    queryset         = Tag.objects.all()
    serializer_class = TagSerializer
    
 

class RequestedItemsViewSet(ModelViewSet):
    serializer_class = RequestedItemsSerializer
    permission_classes=[IsAuthenticated]
    http_method_names = ['get', 'delete', 'post']
    def get_queryset(self):
        return RequestItem.objects.select_related('project', 'parent').filter(parent__user = self.request.user).all()


class VerificationViewSet(ModelViewSet):
    serializer_class = VerificationDocSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return VerificationDoc.objects.select_related('user').filter(user = self.request.user).all()

