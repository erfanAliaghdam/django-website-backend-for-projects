from django.conf import settings
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.db import transaction
from django.db.models import Count, F, Q
from .serializers import (ProjectSerializer, TagSerializer,
                             RequestedItemsSerializer, VerificationDocSerializer,
                             AcceptProjectSerializer, AcceptProjectSerializerReadOnly,
                             MentorMessageSerializer,)
from ..models import Project, Tag, RequestItem, VerificationDoc, MentorMessageForAdmission

from ..permissions import IsMentorOrReadOnly, IsMentor, IsVerifiedUser
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

# Create your views here.



class ProjectViewSet(ModelViewSet):
    serializer_class   = ProjectSerializer
    filter_backends    = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    filterset_fields   = ['tag']
    search_fields      = ['title', 'description']
    permission_classes = [IsMentorOrReadOnly]
    ordering_fields    = ['project__title']


    def get_queryset(self):
        return Project.objects.select_related('user').prefetch_related('tag', 'requests').annotate(
            remaining_admission = F('admissionNo') - Count('requests__id', filter=Q(requests__status = RequestItem.APPROVE))
            ).all()

    def get_serializer_context(self):
        return {'context': self.request}
    @method_decorator(cache_page(60))
    def list(self, request, *args, **kwargs):
        qs = Project.objects.select_related('user').prefetch_related('tag', 'requests').filter(is_active = True).annotate(
            remaining_admission = F('admissionNo') - Count('requests__id', filter=Q(requests__status = RequestItem.APPROVE))
            ).all()
        serializer = ProjectSerializer(qs, many = True, context = {'context': request})
        return Response(serializer.data)

    @action(detail = False, methods=['GET'], permission_classes = [IsAuthenticated, IsMentor], ordering_fields=['project__title', 'project__is_active'])
    def me(self, request):
        if request.method == 'GET':
            project    = Project.objects.select_related('user').prefetch_related('tag').filter(user = self.request.user)
            serializer = ProjectSerializer(project, many = True)
            return Response(serializer.data)


    @action(detail = False, methods=['GET', 'PUT'], permission_classes = [IsAuthenticated, IsMentor], url_path='me/(?P<project_id>[^/.]+)')
    def myProjectDetail(self, request, project_id):
        try:
            project = Project.objects.prefetch_related('tag').select_related('user').get(user = self.request.user, pk = project_id)
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
    permission_classes = [IsAuthenticated, IsVerifiedUser]
    http_method_names  = ['get', 'delete', 'post']
    filter_backends    = [SearchFilter, DjangoFilterBackend]
    filterset_fields   = ['project__tag']
    search_fields      = ['project__title']
    select_related     = ['project', 'parent']
    def get_queryset(self):
        return RequestItem.objects.select_related('project', 'parent').filter(parent__user = self.request.user).all().annotate(
            remaining_admission = F('project__admissionNo') - Count('id', filter=Q(status = RequestItem.APPROVE))
        )

    def destroy(self, request, *args, **kwargs):
        objStatus     = RequestItem.objects.select_related('parent', 'user').filter(pk = self.kwargs['pk']).values('status')[0]['status']
        if objStatus == RequestItem.APPROVE:
            raise ValidationError(code = status.HTTP_403_FORBIDDEN, detail = 'You cannot delete an approved request')
        return super().destroy(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):  
        if 'project_id' not in request.data:
            raise ValidationError(code = status.HTTP_400_BAD_REQUEST, detail = 'Project ID is required')
        if RequestItem.objects.select_related('parent').filter(parent__user = self.request.user, status = RequestItem.APPROVE).count() >= int(settings.MAX_ACCEPTED_APPLY_NO):
            raise ValidationError(code = status.HTTP_406_NOT_ACCEPTABLE, detail = 'You cannot apply for more projects, because you have already ' + str(settings.MAX_ACCEPTED_APPLY_NO) + ' approved active projects')
        return super().create(request, *args, **kwargs)



    # @action(detail = True, methods=['GET', 'PUT'],serializer_class=RequestedItemsSerializer ,permission_classes = [IsAuthenticated, IsMentor], url_name='applied-projects')    
    # def applied(self, request):
    #     if request.method == 'GET':
    #         projects = RequestItem.objects.select_related('project').filter(project__user = self.request.user).all().annotate(
    #             remaining_admission = F('project__admissionNo') - Count('id', filter=Q(status = RequestItem.APPROVE))
    #         )
        #     serializer = RequestedItemsSerializer(projects, many = True)
        #     return Response(serializer.data)
        # elif request.method == 'PUT':
        #     serializer = RequestedItemsSerializer(data = request.data)
        #     serializer.is_valid(raise_exception = True)
        #     serializer.save()
        #     return Response(serializer.data)


class VerificationViewSet(ModelViewSet):
    serializer_class = VerificationDocSerializer
    permission_classes=[IsAuthenticated]
    http_method_names = ['get', 'post']
    def get_queryset(self):
        return VerificationDoc.objects.select_related('user').filter(user = self.request.user).all()


    def list(self, request, *args, **kwargs):
        instance = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(instance,many=True)
        response_data = []
        response_data.extend(serializer.data)
        if self.request.user.is_mentor:
            if self.request.user.profile_mentor.is_verified:
                response_data.append({'verified' : True})
            else: response_data.append({'verified' : False})
        else: 
            if self.request.user.profile_stud.is_verified:
                response_data.append({'verified' : True})
            else: response_data.append({'verified' : False})
        response = Response(response_data)
        return response



class AcceptRequestsViewSet(ModelViewSet):
    serializer_class   = AcceptProjectSerializerReadOnly
    permission_classes = [IsAuthenticated, IsMentor, IsVerifiedUser]
    http_method_names  = ['get', 'post']
    filter_backends    = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields      = ['project__title', 'project__id']
    ordering_fields    = ['project__title']

    def get_queryset(self):
        return RequestItem.objects.select_related('project', 'parent__user').filter(project__user = self.request.user).all().annotate(
            remaining_admission = F('project__admissionNo') - Count('id', filter=Q(status = RequestItem.APPROVE)),
            active_count        = Count('id', filter=Q(status = RequestItem.APPROVE)),
        )
    
    def get_serializer_context(self):
        return {'context': self.request}



    def create(self, request):
        return Response('FORBIDDEN 403', status=status.HTTP_403_FORBIDDEN)




    @action(detail = True, methods=['GET','POST'],serializer_class=AcceptProjectSerializer ,permission_classes = [IsAuthenticated, IsMentor], url_name='cancel')
    def cancel(self, request, *args, **kwargs):
        obj     = self.get_object()
        if obj.passed:
                raise ValidationError(code = status.HTTP_406_NOT_ACCEPTABLE, detail = 'client has finished the project you cannot cancel')
        if request.method == 'GET':
            serializer = AcceptProjectSerializerReadOnly(obj)
            return Response(serializer.data)
        elif request.method == 'POST':
            try:
                with transaction.atomic():
                    obj.status = RequestItem.REJECT
                    obj.save()
                    MentorMessageForAdmission.objects.create(parent = obj, message = request.POST['message'])
                    return Response('Canceled .' ,status = status.HTTP_200_OK)
            except Exception as e:
                print(e)
                return Response('error' , status = status.HTTP_406_NOT_ACCEPTABLE)

    # TODO : add messages action
    @action(detail = True, methods=['GET','POST'],serializer_class=AcceptProjectSerializer ,permission_classes = [IsAuthenticated, IsMentor], url_name='accept')
    def accept(self, request, *args, **kwargs):
        obj     = self.get_object()
        if obj.passed:
                raise ValidationError(code = status.HTTP_406_NOT_ACCEPTABLE, detail = 'client has finished the project you cannot do anything')
        if request.method == 'GET':
            serializer = AcceptProjectSerializerReadOnly(obj)
            return Response(serializer.data)
        elif request.method == 'POST':
            active_count     =  RequestItem.objects.select_related('parent', 'project').filter(parent__user = obj.parent.user , project = obj.project, status = RequestItem.APPROVE).count()
            if active_count >= int(settings.MAX_ACCEPTED_APPLY_NO):
                raise ValidationError(code    = status.HTTP_406_NOT_ACCEPTABLE, detail = 'this user has ' + str(settings.MAX_ACCEPTED_APPLY_NO) + ' active projects choose another student.')
            if obj.remaining_admission <= 0:
                raise ValidationError(code = status.HTTP_406_NOT_ACCEPTABLE, detail = 'Project is full')
            try:
                with transaction.atomic():
                    obj.status = RequestItem.APPROVE
                    obj.save()
                    MentorMessageForAdmission.objects.select_related('parent').create(parent = obj, message = request.POST['message'])
                return Response(status = status.HTTP_201_CREATED)
            except Exception as e:
                print(e)
                return Response('error' , status = status.HTTP_406_NOT_ACCEPTABLE)


class MentorMessageViewSet(ModelViewSet):
    serializer_class   = MentorMessageSerializer
    permission_classes = [IsAuthenticated, IsVerifiedUser]

    def get_queryset(self):
        return MentorMessageForAdmission.objects.select_related('parent').all()

    def get_serializer_context(self):
        return {'context': self.request}

    # @action(detail = True, methods=['GET','POST'],serializer_class=MentorMessageSerializer ,permission_classes = [IsAuthenticated, IsMentor], url_name='reply')
    # def reply(self, request, *args, **kwargs):
    #     obj     = self.get_object()
    #     if request.method == 'GET':
    #         serializer = MentorMessageSerializer(obj)
    #         return Response(serializer.data)
    #     elif request.method == 'POST':
    #         try:
    #             with transaction.atomic():
            #         obj.message = request.POST['message']
            #         obj.save()
            #         return Response('Replied .' ,status = status.HTTP_200_OK)
            # except Exception as e:
            #     print(e)
            #     return Response('error' , status = status.HTTP_406_NOT_ACCEPTABLE)