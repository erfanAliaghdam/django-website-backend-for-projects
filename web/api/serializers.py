from rest_framework import serializers
from ..models import Project, Tag



class ProjectSerializer(serializers.ModelSerializer):
    num_tags = serializers.IntegerField(read_only = True)
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'tag', 'num_tags']
        

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Tag
        fields = ['id', 'name', 'color']

