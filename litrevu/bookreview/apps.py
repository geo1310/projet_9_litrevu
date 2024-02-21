from django.apps import AppConfig

# Définition de la configuration de l'application "bookreview"


class BookreviewConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"  # Définition du champ incrémenté par défaut pour les modèles
    name = "bookreview"  # Nom de l'application
