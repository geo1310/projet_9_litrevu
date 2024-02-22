from django.urls import (
    path,
)  # Importation de fonctions nécessaires pour définir les URL

import bookreview.views

urlpatterns = [
    # URL pour afficher le flux d'activité
    path("flux/", bookreview.views.flux, name="flux"),
    # URL pour afficher les abonnements et les abonnés d'un utilisateur
    path("follows/", bookreview.views.follows, name="follows"),
    # URL pour afficher tous les tickets et critiques de l'utilisateur connecté
    path("posts/", bookreview.views.posts, name="posts"),
    # URL pour supprimer un abonnement d'un utilisateur
    path(
        "follows/<int:follows_id>/delete",
        bookreview.views.follows_delete,
        name="follows_delete",
    ),
    # URL pour créer un nouveau ticket
    path("ticket/create", bookreview.views.create_ticket, name="create_ticket"),
    # URL pour éditer un ticket existant
    path(
        "ticket/<int:ticket_id>/edit", bookreview.views.edit_ticket, name="edit_ticket"
    ),
    # URL pour supprimer un ticket existant
    path(
        "ticket/<int:ticket_id>/delete",
        bookreview.views.delete_ticket,
        name="delete_ticket",
    ),
    # URL pour créer une nouvelle critique
    path("review/create", bookreview.views.create_review, name="create_review"),
    # URL pour éditer une critique existante
    path(
        "review/<int:review_id>/edit", bookreview.views.edit_review, name="edit_review"
    ),
    # URL pour créer une critique pour un ticket spécifique
    path(
        "review/ticket/<int:ticket_id>/create",
        bookreview.views.create_review_ticket,
        name="create_review_ticket",
    ),
    # URL pour supprimer une critique existante
    path(
        "review/<int:review_id>/delete",
        bookreview.views.delete_review,
        name="delete_review",
    ),
]
