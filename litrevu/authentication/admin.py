from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser

# Définition des classes d'administration personnalisées pour chaque modèle


class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "is_active",
        "is_staff",
        "id",
    )
    search_fields = ("username",)


# Enregistrement des classes d'administration personnalisées pour chaque modèle

admin.site.register(CustomUser, CustomUserAdmin)
