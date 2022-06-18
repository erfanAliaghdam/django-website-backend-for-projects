from rest_framework import serializers
from ..models import Project, Tag, RequestedProjects, RequestItem
from django.conf import settings



class ProjectSerializer(serializers.ModelSerializer):
    num_tags = serializers.IntegerField(read_only = True)
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'tag', 'num_tags']
        

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Tag
        fields = ['id', 'name', 'color']



class SimpleProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'tag']
        
class RequestedItemsSerializer(serializers.ModelSerializer):
    project = SimpleProjectSerializer()
    class Meta:
        model  = RequestItem
        fields = ['id', 'project']

class RequestedProjectsSerializer(serializers.ModelSerializer):
    items = RequestedItemsSerializer(many=True, read_only=True)
    class Meta:
        model  = RequestedProjects
        fields = ['items', 'user']
