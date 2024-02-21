from django.apps import AppConfig

# Définition de la configuration de l'application "authentication"


class AuthenticationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"  # Définition du champ incrémenté par défaut pour les modèles
    name = "authentication"  # Nom de l'application
