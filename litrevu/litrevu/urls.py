from django.contrib import admin
from django.urls import (
    path,
    include,
)  # Importation de fonctions nécessaires pour définir les URL
from django.conf import (
    settings,
)  # Importation des paramètres de configuration de Django
from django.conf.urls.static import (
    static,
)  # Importation pour servir les fichiers statiques en développement

urlpatterns = [
    # URL pour l'interface d'administration
    path("admin/", admin.site.urls),
    # Inclusion des URLs de l'application d'authentification
    path("", include("authentication.urls")),
    # Inclusion des URLs de l'application bookreview
    path("", include("bookreview.urls")),
]

# Les images stockées dans le répertoire MEDIA_ROOT seront servies au chemin donné par MEDIA_URL
# Seulement en environnement de développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
