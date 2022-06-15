from rest_framework import serializers
from ..models import Project



class ProjectSerializer(serializers.ModelSerializer):
    num_tags = serializers.IntegerField(read_only = True)
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'tag', 'num_tags']
        

