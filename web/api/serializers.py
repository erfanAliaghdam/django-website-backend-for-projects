from rest_framework import serializers, status
from ..models import Project, Tag, RequestedProjects, RequestItem, VerificationDoc, MentorMessageForAdmission
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError, NotAcceptable


class SimplaUserSerializer(serializers.ModelSerializer):
    class Meta:
        model  = get_user_model()
        fields = ['first_name', 'last_name', 'resume']


class TagSerializer(serializers.ModelSerializer):
    name  = serializers.CharField(read_only=True)
    color = serializers.CharField(read_only=True)

    class Meta:
        model  = Tag
        fields = ['id', 'name', 'color']


class ProjectSerializer(serializers.ModelSerializer):
    num_tags            = serializers.IntegerField(read_only = True)
    user                = SimplaUserSerializer(read_only = True)
    admissionNo         = serializers.IntegerField(required = True)
    is_active           = serializers.BooleanField(read_only = True)
    remaining_admission = serializers.IntegerField(read_only = True)
    
    class Meta:
        model  = Project
        fields = ['id', 'title', 'description', 'tag', 'num_tags', 'user', 'admissionNo', 'is_active', 'remaining_admission']


    def create(self, validated_data):
        validated_data.update({"user":self.context['context'].user})
        return super().create(validated_data)


        
           


class SimpleProjectSerializer(serializers.ModelSerializer):
    title       = serializers.CharField(max_length = 255, read_only = True)
    class Meta:
        model  = Project
        fields = ['id', 'title']

    
        
class RequestedItemsSerializer(serializers.ModelSerializer):
    project             = SimpleProjectSerializer(read_only = True)
    status              = serializers.CharField(read_only = True)
    project_id          = serializers.IntegerField()
    passed              = serializers.BooleanField(read_only = True)
    remaining_admission = serializers.IntegerField(read_only = True)


    class Meta:
        model  = RequestItem
        fields = ['id', 'project', 'status', 'project_id', 'passed', 'remaining_admission']

    def create(self, validated_data):
        project_id    = validated_data.pop('project_id')
        appliedNo     = RequestItem.objects.select_related('project').filter(project__id = project_id, status=RequestItem.APPROVE).count()
        admissionNo   = Project.objects.filter(pk = project_id).values()[0]['admissionNo']
        if Project.objects.get(pk = project_id).is_active == False:
            raise ValidationError('Project is not active yet.')
        if admissionNo <= appliedNo:
            raise NotAcceptable('Admission is over, try another project', code = status.HTTP_406_NOT_ACCEPTABLE)
        #* if request parent doesnt exists od created accidently this try-except block will create new one
        try:
            request_parent = RequestedProjects.objects.get(user = self.context['request'].user)
        except RequestedProjects.DoesNotExist:
            RequestedProjects.objects.create(user = self.context['request'].user) 
        

        #* this block will check if requested current project or not
        if RequestItem.objects.filter(project_id = project_id, parent = request_parent).exists():
            raise ValidationError('Project already requested')

        #* will check if project exists or not if not raise error with message
        try:
            project = Project.objects.get(id = project_id)
        except Project.DoesNotExist:
            raise ValidationError('Project does not exist')
        request_item = RequestItem.objects.create(project = project, parent= request_parent)
        return request_item
    
class VerificationDocSerializer(serializers.ModelSerializer):
    is_accepted = serializers.CharField(read_only = True)
    class Meta:
        model  = VerificationDoc
        fields = ['id', 'document', 'is_accepted']
    def create(self, validated_data):
        verification_doc = VerificationDoc.objects.create(user = self.context['request'].user, document = validated_data['document'])
        return verification_doc   



class SimplaUserSerializer(serializers.ModelSerializer):
    class Meta:
        model  = get_user_model()
        fields = ['first_name', 'last_name', 'resume']





class AcceptProjectSerializer(serializers.ModelSerializer):
    status              = serializers.CharField(read_only = True)
    project             = SimpleProjectSerializer(read_only = True)
    project_id          = serializers.IntegerField(read_only = True)
    user                = serializers.SerializerMethodField(read_only = True)
    message             = serializers.CharField(required = True)
    def get_user(self, obj):
        return SimplaUserSerializer(obj.parent.user).data

    def create(self, validated_data):
        validated_data.pop("message", None)
        return super().create(validated_data)

    class Meta:
        model  = RequestItem
        fields = ['id', 'project',  'status', 'project_id', 'user', 'message']




class AcceptProjectSerializerReadOnly(serializers.ModelSerializer):
    status              = serializers.CharField(read_only = True)
    project             = SimpleProjectSerializer(read_only = True)
    project_id          = serializers.IntegerField(read_only = True)
    user                = serializers.SerializerMethodField(read_only = True)
    def get_user(self, obj):
        return SimplaUserSerializer(obj.parent.user).data

    class Meta:
        model  = RequestItem
        fields = ['id', 'project', 'status', 'project_id', 'user']


class MentorMessageSerializer(serializers.ModelSerializer):    
    class Meta:
        model  = MentorMessageForAdmission
        fields = ['id', 'message', 'parent']

