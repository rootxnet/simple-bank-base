from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class CustomUserAdmin(UserAdmin):
    list_display = [
        "username",
        "first_name",
        "last_name",
        "email",
    ]
    list_search = (
        "username",
        "email",
        "first_name",
        "last_name",
    )

    class Meta:
        model = User


admin.site.register(User, CustomUserAdmin)
