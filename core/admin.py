from django.contrib import admin
from django.template.defaultfilters import truncatewords
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from web.admin import TublarDocument, TublarMentor, TublarStudent
from .models import User, Message
from .filters import MentorVerificationFilter


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("password1", "password2", "phone", "first_name", "last_name", "is_mentor"),
            },
        ),
    )
    #* ------------------------------
    list_display = ("phone", "is_mentor" , "first_name", "last_name", "otp_activated")
    #* ------------------------------
    fieldsets = (
        (None, {"fields": ("phone", "password")}),
        (("Personal Info"), {"fields": ("first_name", "last_name")}),
        (
            ("Permissions"),
            {
                "fields": (
                    "otp_activated",
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
    list_filter = ("is_staff", "is_superuser", "is_active", "groups", "is_mentor", "otp_activated", "profile_stud__is_verified", MentorVerificationFilter)
    search_fields = ['first_name', 'last_name', 'phone']
    actions_on_bottom = True
    #* ------------------------------
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('profile_stud', 'profile_mentor')
    #* ------------------------------
    
    def get_inlines(self, request, obj):
        if obj is None:
            return []
        elif obj.is_mentor:
            return [TublarDocument, TublarMentor]
        return [TublarStudent]




@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display        = ("message_type", "send_time", "get_message")
    list_filter         = ("message_type", "send_time")
    search_fields       = ("reciever__phone", "reciever__first_name", "reciever__last_name")
    autocomplete_fields = ['reciever']

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('reciever').all()
    def get_message(self, obj):
        return truncatewords(obj.message, 10)


