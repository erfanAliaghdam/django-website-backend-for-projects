from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from web.admin import TublarDocument, TublarMentor, TublarStudent


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", "phone", "first_name", "last_name"),
            },
        ),
    )

    inlines = [TublarDocument, TublarStudent, TublarMentor]
