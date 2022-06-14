from django.shortcuts import render
from requests import Response
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Count
from .serializers import (ProjectSerializer)
from .models import Project, RequestItem
from .permissions import IsAdminOrReadOnly
# Create your views here.




class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    queryset         = Project.objects.prefetch_related('tag').all().annotate(
        num_tags=Count('tag')
    )
    filter_backends    = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    filterset_fields   = ['tag']
    search_fields      = ['title', 'description']
    ordering_fields    = ['num_tags']    
    permission_classes = [IsAdminOrReadOnly]

    def num_tags(self, obj):
        return obj.num_tags







