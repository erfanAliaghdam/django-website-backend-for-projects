from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.generics import ListAPIView
from django.db.models import Count
from .serializers import (ProjectSerializer, TagSerializer)
from ..models import Project, Tag
from ..permissions import IsAdminOrReadOnly
# Create your views here.




class ProjectViewSet(ModelViewSet):
    queryset         = Project.objects.prefetch_related('tag').all().annotate(
        num_tags=Count('tag')
    )
    serializer_class   = ProjectSerializer
    filter_backends    = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    filterset_fields   = ['tag']
    search_fields      = ['title', 'description']
    ordering_fields    = ['num_tags']    
    permission_classes = [IsAdminOrReadOnly]

    def num_tags(self, obj):
        return obj.num_tags
    
class TagViewSet(ReadOnlyModelViewSet):
    queryset         = Tag.objects.all()
    serializer_class = TagSerializer
    
 



