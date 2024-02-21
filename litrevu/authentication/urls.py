from django.urls import (
    path,
)  # Importation de fonctions nécessaires pour définir les URL

# Import des vues génériques de l'authentification
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView,
)

import authentication.views

urlpatterns = [
    # URL pour la page de connexion
    path(
        "",
        LoginView.as_view(
            template_name="authentication/login.html", redirect_authenticated_user=True
        ),
        name="login",
    ),
    # URL pour la page d'inscription
    path("signup/", authentication.views.signup, name="signup"),
    # URL pour la déconnexion
    path("logout/", LogoutView.as_view(), name="logout"),
    # URL pour la modification de mot de passe
    path(
        "change-password/",
        PasswordChangeView.as_view(
            template_name="authentication/password_change_form.html"
        ),
        name="password_change",
    ),
    # URL pour la confirmation de modification de mot de passe
    path(
        "change-password-done/",
        PasswordChangeDoneView.as_view(
            template_name="authentication/password_change_done.html"
        ),
        name="password_change_done",
    ),
]
