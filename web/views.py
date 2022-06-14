from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import (ProjectSerializer)
from .models import Project
# Create your views here.




class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.prefetch_related('tag').all()
