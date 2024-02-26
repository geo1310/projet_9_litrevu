from django.contrib.auth.models import (
    AbstractUser,
)  # Importation du modèle d'utilisateur abstrait de Django


class CustomUser(AbstractUser):
    """
    Modèle personnalisé d'utilisateur.

    Utilise le modèle d'utilisateur abstrait de Django pour étendre les fonctionnalités de base.

    Attributes:
        username: Nom d'utilisateur unique.
        first_name: Prénom de l'utilisateur.
        last_name: Nom de famille de l'utilisateur.
        email: Adresse e-mail de l'utilisateur.
        password: Mot de passe de l'utilisateur (haché).
        date_joined: Date et heure de création du compte utilisateur.
        is_active: Indique si le compte utilisateur est actif ou non.
        is_staff: Indique si l'utilisateur est membre du personnel ou non.
        is_superuser: Indique si l'utilisateur a tous les droits de l'administrateur ou non.
    """

    pass
