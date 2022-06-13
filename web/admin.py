from django.contrib import admin
from django.utils.html import format_html
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


admin.site.register(models.ProfileMentor)
admin.site.register(models.ProfileStud)
admin.site.register(models.Tag)
admin.site.register(models.Project)