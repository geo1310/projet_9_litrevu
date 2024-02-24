import bookreview.views
from django.urls import path

urlpatterns = [
    path("flux/", bookreview.views.flux, name="flux"),
    path("follows/", bookreview.views.follows, name="follows"),
    path("posts/", bookreview.views.posts, name="posts"),
    path(
        "follows/<int:follows_id>/delete",
        bookreview.views.follows_delete,
        name="follows_delete",
    ),
    path("ticket/create", bookreview.views.create_ticket, name="create_ticket"),
    path(
        "ticket/<int:ticket_id>/edit", bookreview.views.edit_ticket, name="edit_ticket"
    ),
    path(
        "ticket/<int:ticket_id>/delete",
        bookreview.views.delete_ticket,
        name="delete_ticket",
    ),
    path("review/create", bookreview.views.create_review, name="create_review"),
    path(
        "review/<int:review_id>/edit", bookreview.views.edit_review, name="edit_review"
    ),
    path(
        "review/ticket/<int:ticket_id>/create",
        bookreview.views.create_review_ticket,
        name="create_review_ticket",
    ),
    path(
        "review/<int:review_id>/delete",
        bookreview.views.delete_review,
        name="delete_review",
    ),
]
