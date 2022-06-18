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
        model  = Project
        fields = ['id', 'title']
        
class RequestedItemsSerializer(serializers.ModelSerializer):
    project = SimpleProjectSerializer()
    status  = serializers.CharField(read_only = True)
    class Meta:
        model  = RequestItem
        fields = ['id', 'project', 'status']


