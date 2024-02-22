from django.contrib.auth import (
    get_user_model,
)  # Importation de la fonction pour obtenir le modèle utilisateur

from django.contrib.auth.forms import (
    UserCreationForm,
)  # Importation du formulaire de création d'utilisateur


class SignupForm(UserCreationForm):
    """
    Formulaire d'inscription personnalisé.

    Utilise le modèle d'utilisateur par défaut et se limite au champ 'username'.

    Attributes:
        Meta: Classe interne pour définir les métadonnées du formulaire.
            model: Modèle d'utilisateur à utiliser pour l'inscription.
            fields: Champs du formulaire à afficher (seulement 'username' dans ce cas).
    """

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("username",)
