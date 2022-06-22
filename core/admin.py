from django.contrib import admin
from django.template.defaultfilters import truncatewords
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from web.admin import TublarDocument, TublarMentor, TublarStudent
from .models import User, Message


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", "phone", "first_name", "last_name", "is_mentor"),
            },
        ),
    )
    #* ------------------------------
    list_display = ("username", "is_mentor", "phone", "first_name", "last_name")
    #* ------------------------------
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (("Personal info"), {"fields": ("first_name", "last_name", "phone")}),
        (
            ("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_mentor",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    #* ------------------------------
    list_filter = ("is_staff", "is_superuser", "is_active", "groups", "is_mentor", "profile__is_verified")
    search_fields = ['username', 'first_name', 'last_name', 'phone']
    #* ------------------------------
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('profile')
    #* ------------------------------

    def get_inlines(self, request, obj):
        if obj is None:
            return []
        elif obj.is_mentor:
            print(self.get_changelist_instance)
            return [TublarDocument, TublarMentor]
        return [TublarStudent]



@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display        = ("id", "message_type", "send_time", "get_message")
    list_filter         = ("message_type", "send_time")
    search_fields       = ("reciever__username", "reciever__first_name", "reciever__last_name")
    autocomplete_fields = ['reciever']
    def get_message(self, obj):
        return truncatewords(obj.message, 10)