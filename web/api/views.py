from django.conf import settings
from rest_framework import status, mixins
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.db import transaction
from django.db.models import Count, Value, F, Q
from core.api.serializers import MessageSerializer
from .serializers import (ProjectSerializer, TagSerializer,
                             RequestedItemsSerializer, VerificationDocSerializer,
                             AcceptProjectSerializer, AcceptProjectSerializerReadOnly,
                             MentorMessageSerializer)
from ..models import ApprovedItem, ApprovedRequest, Project, Tag, RequestItem, VerificationDoc, MessageForAdmission

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
        return RequestItem.objects.select_related('project', 'parent').filter(parent__user = self.request.user).all().annotate(
            remaining_admission = F('project__admissionNo') - Count('id', filter=Q(status = RequestItem.APPROVE))
        )



    def destroy(self, request, *args, **kwargs):
        objStatus     = RequestItem.objects.select_related('parent').filter(pk = self.kwargs['pk']).values('status')[0]['status']
        if objStatus == RequestItem.APPROVE:
            raise ValidationError(code = status.HTTP_406_NOT_ACCEPTABLE, detail = 'You cannot delete an approved request')
        return super().destroy(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        if 'project_id' not in request.data:
            raise ValidationError(code = status.HTTP_400_BAD_REQUEST, detail = 'Project ID is required')
        if RequestItem.objects.select_related('parent').filter(parent__user = self.request.user, status = RequestItem.APPROVE).count() >= int(settings.MAX_ACCEPTED_APPLY_NO):
            raise ValidationError(code = status.HTTP_406_NOT_ACCEPTABLE, detail = 'You cannot apply for more projects, because you have already ' + str(settings.MAX_ACCEPTED_APPLY_NO) + ' approved active projects')
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
    filter_backends    = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields      = ['project__title', 'project__id']
    ordering_fields    = ['project__title']
    def get_queryset(self):
        return RequestItem.objects.select_related('project', 'parent__user').filter(project__user = self.request.user).all()
    
    def get_serializer_context(self):
        return {'context': self.request}



    def create(self, request):
        return Response('FORBIDDEN 403', status=status.HTTP_403_FORBIDDEN)


    @action(detail = True, methods=['GET','POST'],serializer_class=AcceptProjectSerializer ,permission_classes = [IsAuthenticated, IsMentor], url_name='cancel')
    def cancel(self, request, *args, **kwargs):
        obj     = self.get_object()
        project = obj.project.id
        student = obj.parent.user.id
        if ApprovedItem.objects.select_related('parent').filter(parent__user__pk = student, project__pk = project, status = ApprovedItem.PASSED).exists():
                raise ValidationError(code = status.HTTP_406_NOT_ACCEPTABLE, detail = 'client has finished the project you cannot cancel')
        if request.method == 'GET':
            serializer = AcceptProjectSerializerReadOnly(obj)
            return Response(serializer.data)
        elif request.method == 'POST':
            try:
                with transaction.atomic():
                    approvedItem        = ApprovedItem.objects.select_related('parent', 'project').get(parent__user__pk = student, project__pk = project, status = ApprovedItem.APPROVE)
                    approvedItem.status = ApprovedItem.REJECT
                    approvedItem.save()
                    obj.status = RequestItem.REJECT
                    obj.save()
                    MessageForAdmission.objects.create(parent = approvedItem, message = request.POST['message'])
                    print('----DONE----')
                    return Response('Canceled .' ,status = status.HTTP_200_OK)
            except Exception as e:
                print(e)
                return Response('error' , status = status.HTTP_406_NOT_ACCEPTABLE)


    @action(detail = True, methods=['GET','POST'],serializer_class=AcceptProjectSerializer ,permission_classes = [IsAuthenticated, IsMentor], url_name='accept')
    def accept(self, request, *args, **kwargs):
        print('----ACCEPT----')
        obj     = self.get_object()
        project = obj.project
        student = obj.parent.user
        if ApprovedItem.objects.select_related('parent', 'project').filter(parent__user = student, project = project, status = ApprovedItem.PASSED).exists():
                raise ValidationError(code = status.HTTP_406_NOT_ACCEPTABLE, detail = 'client has finished the project you cannot do anything')
        if request.method == 'GET':
            serializer = AcceptProjectSerializerReadOnly(obj)
            return Response(serializer.data)
        print('-----||||-----')

        student_active_approved_count     = ApprovedRequest.objects.prefetch_related('items').filter(user = student, items__status = ApprovedItem.APPROVE).count()

        if student_active_approved_count >= int(settings.MAX_ACCEPTED_APPLY_NO):
            raise ValidationError(code    = status.HTTP_406_NOT_ACCEPTABLE, detail = 'this user has ' + str(settings.MAX_ACCEPTED_APPLY_NO) + ' active projects choose another student.')
        
        
        active_approved_count = ApprovedItem.objects.filter(project = project, parent__user = student ,status = ApprovedItem.APPROVE).count()
        if project.admissionNo <= active_approved_count:
            raise ValidationError(code = status.HTTP_406_NOT_ACCEPTABLE, detail = 'Project is full')

        if not hasattr(student, 'approved_projects_cart'):
            parent   = ApprovedRequest.objects.create(user = student)
        else: parent = student.approved_projects_cart
        try:
            with transaction.atomic():
                approve, _ = ApprovedItem.objects.get_or_create(parent = parent, project = project)
                approve.status = ApprovedItem.APPROVE
                approve.save()
                obj.status = RequestItem.APPROVE
                obj.save()
                MessageForAdmission.objects.create(parent = approve, message = request.POST['message'])
            return Response(status = status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response('error' , status = status.HTTP_406_NOT_ACCEPTABLE)
