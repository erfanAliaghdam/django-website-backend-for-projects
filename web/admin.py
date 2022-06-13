from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from . import models
# Register your models here.


class TublarMentor(admin.TabularInline):
    model = models.ProfileMentor

class TublarStudent(admin.TabularInline):
    model  = models.ProfileStud

class TublarDocument(admin.TabularInline):
    model  = models.VerificationDoc
    readonly_fields = ['thumbnail']
    extra = 1
    def thumbnail(self, instance):
        if instance.document.name != '':
            return format_html(f'<a href={instance.document.url}><img src={instance.document.url} style="width:100px;height:100px;object-fit:cover;border-radius:8px;" /></a>')
        return " "


@admin.register(models.RequestedProjects)
class RequestedProjectAdmin(admin.ModelAdmin):
    model = models.RequestedProjects
    readonly_fields = ['id']
    list_select_related = ['user']
    list_display = ['username']

    def username(self, obj):
        return obj.user.username

@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    model = models.Tag
    list_display = ['name', 'color_format', 'projects_count']
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('projects').annotate(
            proj_count = Count('projects')
        )
    def color_format(self, obj):
        return format_html(f"<b style='color:{obj.color};background-color:black;text-decoration:bold;border-radius:3px;padding:2px;'>{obj.color}</b>")


    def projects_count(self, obj):
        return obj.proj_count
admin.site.register(models.Project)