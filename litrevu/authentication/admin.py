from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "is_active",
        "is_staff",
        "id",
    )
    search_fields = ("username",)


# Enregistrez votre CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)
