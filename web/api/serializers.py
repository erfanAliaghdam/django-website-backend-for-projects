from rest_framework import serializers
from ..models import Project, Tag, RequestedProjects, RequestItem, VerificationDoc
from django.conf import settings
from core.api.serializers import UserSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Tag
        fields = ['id', 'name', 'color']


class ProjectSerializer(serializers.ModelSerializer):
    num_tags = serializers.IntegerField(read_only = True)
    user     = UserSerializer(read_only = True)
    tag      = TagSerializer(many = True, read_only = True)
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'tag', 'num_tags', 'user']


    def create(self, validated_data):
        validated_data.update({"user":self.context['context'].user})
        return super().create(validated_data)


        
           


class SimpleProjectSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length = 255, read_only = True)
    class Meta:
        model  = Project
        fields = ['id', 'title']
        
class RequestedItemsSerializer(serializers.ModelSerializer):
    project    = SimpleProjectSerializer(read_only = True)
    status     = serializers.CharField(read_only = True)
    project_id = serializers.IntegerField()
    class Meta:
        model  = RequestItem
        fields = ['id', 'project', 'status', 'project_id']

    

    def create(self, validated_data):
        project_id = validated_data.pop('project_id')
        #* if request parent doesnt exists od created accidently this try-except block will create new one
        try:
            request_parent = RequestedProjects.objects.get(user = self.context['request'].user)
        except RequestedProjects.DoesNotExist:
            RequestedProjects.objects.create(user = self.context['request'].user) 
        

        #* this block will check if requested current project or not
        if RequestItem.objects.filter(project_id = project_id, parent = request_parent).exists():
            raise serializers.ValidationError('Project already requested')

        #* will check if project exists or not if not raise error with message
        try:
            project = Project.objects.get(id = project_id)
        except Project.DoesNotExist:
            raise serializers.ValidationError('Project does not exist')
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