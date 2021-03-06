from tabnanny import verbose
from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, F
from django.template.defaultfilters import truncatechars
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

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
    readonly_fields = ['id']
    list_select_related = ['user']
    list_display = ['phone']
    inlines = [TublarRequestProjectItems]
    search_fields = ['user__phone']
    autocomplete_fields = ['user']
    list_select_related = ['user']
    list_filter = ['items__created_at']
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('items').select_related('user')
    def phone(self, obj):
        return str(obj.user.phone)


@admin.register(models.RequestItem)
class RequestItemAdmin(admin.ModelAdmin):
    model       = models.RequestItem
    list_display        = ['project_title', 'project_mentor', 'requested_user', 'created_at']
    list_filter         = ['created_at', 'passed_time', 'approved_time']
    search_fields       = ['project__title', 'parent__user__phone', 'project__user__phone']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('project', 'parent', 'parent__user', 'project__user')
    def project_title(self, obj):
        return str(truncatechars(obj.project.title, 10))
    def project_mentor(self, obj):
        return str(obj.project.user)
    def requested_user(self, obj):
        return str(obj.parent.user)


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
    fields        = ['title', 'user', 'slug', 'admissionNo', 'description', 'is_active', 'tag']
    list_display  = ['title', 'applied_count', 'admissionNo', 'is_active']
    search_fields = ['title', 'description', 'tag__name', 'user__phone']
    list_filter   = [TagAutoCompleteFilter, 'is_active']
    list_editable = ['is_active']
    filter_horizontal = ('tag',)
    autocomplete_fields = ['user']
    ordering = ['title', 'created_at']
    # TODO : use better filters package and add search to filters box.
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user').prefetch_related('requests', 'tag').annotate(
            applied_No = Count('requests__id')
        )

    def applied_count(self, obj):
        return obj.applied_No





# @admin.register(models.ApprovedRequest)
# class ApprovedRequestAdmin(admin.ModelAdmin):
    # model = models.ApprovedRequest
    # list_display = ['user', 'project_count', 'active_project_count']
    # search_fields = ['user__phone']
    # autocomplete_fields = ['user']
    # list_select_related = ['user']
    # inlines = [TublarApprovedItem]
    # def get_queryset(self, request):
    #     return super().get_queryset(request).select_related('user').prefetch_related('items').annotate(
    #         proj_count = Count('items'),
    #         active_proj_count = Count('items__status', filter=Q(items__status=models.ApprovedItem.APPROVE))
    #     )

    # def project_count(self, obj):
    #     return obj.proj_count

    # def active_project_count(self, obj):
    #     return obj.active_proj_count

@admin.register(models.MentorMessageForAdmission)
class MessageForAdmissionAdmin(admin.ModelAdmin):
    model               = models.MentorMessageForAdmission
    fields              = ['message']
    list_display        = ['user_phone', 'message']
    search_fields       = ['parent__parent__user__phone']
    list_select_related = ['parent__parent__user']
    
    # def __str__(self) -> str:
    #     return super().__str__().parent.parent.user.phone

    def message(self, obj):
        return truncatechars(obj.message, 20)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('parent__parent__user')


    def user_phone(self, obj):
        return obj.parent.parent.user.phone
