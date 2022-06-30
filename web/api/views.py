from django.conf import settings
from rest_framework import status, mixins
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from django.db.models import Count
from .serializers import (ProjectSerializer, TagSerializer,
                             RequestedItemsSerializer, VerificationDocSerializer,
                             AcceptProjectSerializer, AcceptProjectSerializerReadOnly)
from ..models import ApprovedItem, ApprovedRequest, Project, Tag, RequestItem, VerificationDoc

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
    serializer_class   = RequestedItemsSerializer
    permission_classes = [IsAuthenticated]
    http_method_names  = ['get', 'delete', 'post']
    def get_queryset(self):
        return RequestItem.objects.select_related('project', 'parent').filter(parent__user = self.request.user).all()

    def destroy(self, request, *args, **kwargs):
        objStatus     = RequestItem.objects.select_related('parent').filter(pk = self.kwargs['pk']).values('status')[0]['status']
        if objStatus == RequestItem.APPROVED:
            raise ValidationError(code = status.HTTP_406_NOT_ACCEPTABLE, detail = 'You cannot delete an approved request')
        return super().destroy(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        if 'project_id' not in request.data:
            raise ValidationError(code = status.HTTP_400_BAD_REQUEST, detail = 'Project ID is required')
        if RequestItem.objects.select_related('parent').filter(parent__user = self.request.user, status = RequestItem.APPROVED).count() >= int(settings.MAX_ACCEPTED_APPLY_NO):
            raise ValidationError(code = status.HTTP_406_NOT_ACCEPTABLE, detail = 'You cannot apply for more projects, because you have already ' + str(settings.MAX_ACCEPTED_APPLY_NO) + ' approved projects')
        return super().create(request, *args, **kwargs)

class VerificationViewSet(ModelViewSet):
    serializer_class = VerificationDocSerializer
    permission_classes=[IsAuthenticated]
    http_method_names = ['get', 'post']
    def get_queryset(self):
        return VerificationDoc.objects.select_related('user').filter(user = self.request.user).all()


class AcceptRequestsViewSet(ModelViewSet):
    serializer_class   = AcceptProjectSerializerReadOnly
    permission_classes = [IsAuthenticated, IsMentor]
    http_method_names  = ['get', 'post']
    filter_backends    = [SearchFilter, OrderingFilter]
    search_fields      = ['project__title', 'project__id']
    ordering_fields    = ['project__title']
    def get_queryset(self):
        return RequestItem.objects.select_related('project', 'parent__user').filter(project__user = self.request.user).all()
    
    def get_serializer_context(self):
        return {'context': self.request}


    def create(self, request):
        return Response('FORBIDDEN 403', status=status.HTTP_403_FORBIDDEN)

    @action(detail = False, methods=['GET','POST'],serializer_class=AcceptProjectSerializer ,permission_classes = [IsAuthenticated, IsMentor], url_name='accept', url_path='(?P<pk>[^/.]+)')
    def accept(self, request, *args, **kwargs):
        if request.method == 'GET':
            serializer = AcceptProjectSerializerReadOnly(self.get_object())
            return Response(serializer.data)
        print('-----||||-----')
        student = self.get_object().parent.user
        project = self.get_object().project

        student_active_approved_count = ApprovedRequest.objects.filter(user = student, items__status = ApprovedItem.ACTIVE).count()
        if student_active_approved_count >= int(settings.MAX_ACCEPTED_APPLY_NO):
            raise ValidationError(code = status.HTTP_406_NOT_ACCEPTABLE, detail = 'this user has ' + str(settings.MAX_ACCEPTED_APPLY_NO) + ' active projects choose another student.')
        
        
        active_approved_count = ApprovedItem.objects.filter(project = project, status = ApprovedItem.ACTIVE).count()
        if project.admissionNo <= active_approved_count:
            raise ValidationError(code = status.HTTP_406_NOT_ACCEPTABLE, detail = 'Project is full')

        if not hasattr(student, 'approved_projects_cart'):
            parent = ApprovedRequest.objects.create(user = student)
        else: parent = student.approved_projects_cart
        
        ApprovedItem.objects.create(parent = parent, project = project)

        return Response(status = status.HTTP_201_CREATED)