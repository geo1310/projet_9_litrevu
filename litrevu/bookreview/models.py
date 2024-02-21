from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
)  # Importation des validateurs
from django.conf import settings  # Importation des paramètres du projet Django
from django.db import models  # Importation des modèles Django


class Ticket(models.Model):
    """
    Modèle pour les tickets.

    Attributes:
        title (CharField): Titre du ticket.
        description (TextField): Description détaillée du ticket.
        user (ForeignKey): Clé étrangère vers le modèle d'utilisateur pour associer le ticket à un utilisateur.
        image (ImageField): Champ pour télécharger une image liée au ticket.
        time_created (DateTimeField): Date et heure de création du ticket.
    """

    title = models.CharField(max_length=128, verbose_name="Titre")
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(verbose_name="Image")
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def has_review(self):
        """
        Vérifie si ce ticket a une critique associée.
        Retourne True si une critique existe pour ce ticket, False sinon.
        """
        return self.review_set.exists()


class Review(models.Model):
    """
    Modèle pour les critiques.

    Attributes:
        ticket (ForeignKey): Clé étrangère vers le modèle Ticket pour associer la critique à un ticket.
        rating (PositiveSmallIntegerField): Note attribuée à la critique.
        headline (CharField): Titre de la critique.
        body (TextField): Corps de la critique (commentaire).
        user (ForeignKey): Clé étrangère vers le modèle d'utilisateur pour associer la critique à un utilisateur.
        time_created (DateTimeField): Date et heure de création de la critique.
    """

    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)], verbose_name="Note"
    )
    headline = models.CharField(max_length=128, verbose_name="Titre")
    body = models.TextField(max_length=8192, blank=True, verbose_name="Commentaire")
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.headline


class UserFollows(models.Model):
    """
    Modèle pour les utilisateurs suivis.

    Attributes:
        user (ForeignKey): Clé étrangère vers le modèle d'utilisateur pour représenter l'utilisateur qui suit.
        followed_user (ForeignKey): Clé étrangère vers le modèle d'utilisateur pour représenter l'utilisateur suivi.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="following"
    )
    followed_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="followed_by"
    )

    class Meta:
        # Contrainte pour assurer l'unicité des paires utilisateur-utilisateur_suivi
        unique_together = (
            "user",
            "followed_user",
        )
