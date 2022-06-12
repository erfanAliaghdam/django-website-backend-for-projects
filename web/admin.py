from django.contrib import admin
from django.utils.html import format_html
from . import models
# Register your models here.


class TublarMentor(admin.ModelAdmin):
    model = models.ProfileMentor
    
class TublarStudent(admin.ModelAdmin):
    model  = models.ProfileStud



class TublarDocument(admin.TabularInline):
    model  = models.VerificationDoc
    readonly_fields = ['thumbnail']


    def thumbnail(self, instance):
        if instance.image.name != '':
            return format_html(f'<img src={instance.image.url} style="width:100px;height:100px;object-fit:cover;" />')
        return " "


admin.site.register(models.ProfileMentor)
admin.site.register(models.ProfileStud)
admin.site.register(models.Tag)
admin.site.register(models.Project)