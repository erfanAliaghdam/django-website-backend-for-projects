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

    def thumbnail(self, instance):
        if instance.document.name != '':
            return format_html(f'<a href={instance.document.url}><img src={instance.document.url} style="width:100px;height:100px;object-fit:cover;" /></a>')
        return " "


admin.site.register(models.ProfileMentor)
admin.site.register(models.ProfileStud)
admin.site.register(models.Tag)
admin.site.register(models.Project)