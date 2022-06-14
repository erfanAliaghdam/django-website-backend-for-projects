from dataclasses import fields
from rest_framework import serializers
from .models import Project, Tag



class ProjectSerializer(serializers.ModelSerializer):
    num_tags = serializers.IntegerField()
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'tag', 'num_tags']
        

    