from django import forms

from .models import Review, Ticket, UserFollows


class UserFollowsForm(forms.ModelForm):
    """
    Formulaire de suivi d'utilisateur.

    Permet à un utilisateur de suivre un autre utilisateur.

    Attributes:
        Meta: Classe interne pour définir les métadonnées du formulaire.
            model: Modèle associé au formulaire.
            fields: Champs du formulaire à afficher.
            labels: Étiquettes personnalisées pour les champs du formulaire.
    """

    class Meta:
        model = UserFollows
        fields = ["followed_user"]
        labels = {
            "followed_user": "Choisir utilisateur",
        }


class TicketForm(forms.ModelForm):
    """
    Formulaire de création/modification de ticket.

    Permet de créer ou de modifier un ticket.

    Attributes:
        Meta: Classe interne pour définir les métadonnées du formulaire.
            model: Modèle associé au formulaire.
            fields: Champs du formulaire à afficher.
    """

    # champ caché ( utile si utilisation de plusieurs formulaires avec une seule requete POST)
    edit_ticket = forms.BooleanField(
        widget=forms.HiddenInput, initial=True, required=False
    )

    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]


class DeleteTicketForm(forms.Form):
    """
    Formulaire de suppression de ticket.

    Permet de marquer un ticket pour suppression.

    Attributes:
        delete_ticket: Champ booléen caché pour marquer le ticket à supprimer.
    """

    # champ caché ( utile si utilisation de plusieurs formulaires avec une seule requete POST)
    delete_ticket = forms.BooleanField(
        widget=forms.HiddenInput, initial=True, required=False
    )


class ReviewForm(forms.ModelForm):
    """
    Formulaire de création/modification de critique.

    Permet de créer ou de modifier une critique.

    Attributes:
        Meta: Classe interne pour définir les métadonnées du formulaire.
            model: Modèle associé au formulaire.
            fields: Champs du formulaire à afficher.
            widgets: Widgets personnalisés pour les champs du formulaire.
    """

    class Meta:
        model = Review
        fields = ["headline", "rating", "body"]

        widgets = {
            "rating": forms.RadioSelect(
                choices=[(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")]
            ),
        }
