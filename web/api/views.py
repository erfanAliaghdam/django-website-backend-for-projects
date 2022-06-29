from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from django.db.models import Count
from .serializers import (ProjectSerializer, TagSerializer,
                             RequestedItemsSerializer, VerificationDocSerializer,
                             AcceptProjectSerializer)
from ..models import Project, Tag, RequestItem, VerificationDoc

from ..permissions import IsMentorOrReadOnly, IsMentor

# Create your views here.




class ProjectViewSet(ModelViewSet):
    queryset           = Project.objects.prefetch_related('tag', 'user').all().annotate(
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
    def get_serializer_context(self):
        return {'context': self.request}
    
    @action(detail = False, methods=['GET'], permission_classes = [IsAuthenticated, IsMentor])
    def me(self, request):
        if request.method == 'GET':
            project    = Project.objects.filter(user = self.request.user)
            serializer = ProjectSerializer(project, many = True)
            return Response(serializer.data)


    @action(detail = False, methods=['GET', 'PUT'], permission_classes = [IsAuthenticated], url_path='me/(?P<project_id>[^/.]+)')
    def myProjectDetail(self, request, project_id):
        try:
            project = Project.objects.get(user = self.request.user, pk = project_id)
        except Project.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)
        if request.method == 'GET':
            serializer = ProjectSerializer(project, read_only = True)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = ProjectSerializer(project, data = request.data)
            serializer.is_valid(raise_exception = True)
            serializer.save()
            return Response(serializer.data)


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
    http_method_names = ['get', 'post']
    def get_queryset(self):
        return VerificationDoc.objects.select_related('user').filter(user = self.request.user).all()

class AcceptRequestsViewSet(ModelViewSet):
    serializer_class   = AcceptProjectSerializer
    permission_classes = [IsAuthenticated, IsMentor]
    http_method_names  = ['get', 'put']
    def get_queryset(self):
        return RequestItem.objects.select_related('project', 'parent__user').filter(project__user = self.request.user).all()
    
    def get_serializer_context(self):
        return {'context': self.request}