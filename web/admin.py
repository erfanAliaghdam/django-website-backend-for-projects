from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from .filters import TagAutoCompleteFilter
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

class TublarRequestProjectItems(admin.TabularInline):
    model = models.RequestItem
    extra = 1
    autocomplete_fields = ['project']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('project')

@admin.register(models.RequestedProjects)
class RequestedProjectAdmin(admin.ModelAdmin):
    model = models.RequestedProjects
    readonly_fields = ['id', 'user']
    list_select_related = ['user']
    list_display = ['phone']
    inlines = [TublarRequestProjectItems]
    def phone(self, obj):
        return str(obj.user.phone)

@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ['name']
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
    
@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    model = models.Project
    prepopulated_fields = {'slug': ('title',), }
    fields        = ['title', 'user', 'slug', 'description', 'is_active', 'tag']
    list_display  = ['title', 'applied_count', 'is_active']
    search_fields = ['title', 'description', 'tag__name']
    list_filter   = [TagAutoCompleteFilter]
    list_editable = ['is_active']
    filter_horizontal = ('tag',)
    autocomplete_fields = ['user']
    # TODO : use better filters package and add search to filters box.
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('requests', 'user').annotate(
            applied_No = Count('requests')
        )

    def applied_count(self, obj):
        return obj.applied_No


class ApprovedItemTublar(admin.TabularInline):
    model = models.ApprovedItem
    extra = 0
    autocomplete_fields = ['project']



@admin.register(models.ApprovedRequest)
class ApprovedRequest(admin.ModelAdmin):
    model        = models.ApprovedRequest
    list_display = ['user']
    inlines      = [ApprovedItemTublar]
    list_filter  = ('items__status',)
    list_display_links = ['user']

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('items')

