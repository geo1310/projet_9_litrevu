from django.conf import settings
from django.contrib.auth import (
    login,
)  # Importation de la fonction de connexion utilisateur
from django.shortcuts import redirect, render

from . import forms


def signup(request):
    """
    Vue pour l'inscription des utilisateurs.

    Permet aux utilisateurs de s'inscrire à l'application.
    Après une inscription réussie, l'utilisateur est automatiquement connecté
    et redirigé vers la page définie dans LOGIN_REDIRECT_URL.

    Args:
        request: Objet HttpRequest contenant les données de la requête HTTP.

    Returns:
        HttpResponse: Renvoie le rendu de la page d'inscription avec le formulaire.

    """
    form = forms.SignupForm()

    if request.method == "POST":
        form = forms.SignupForm(request.POST)

        if form.is_valid():
            user = form.save()
            # auto-login user
            login(request, user)

            return redirect(settings.LOGIN_REDIRECT_URL)

    return render(request, "authentication/signup.html", context={"form": form})
