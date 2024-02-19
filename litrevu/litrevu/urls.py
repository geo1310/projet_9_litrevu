from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

# vue generique
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView,
)

import authentication.views
import bookreview.views

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "",
        LoginView.as_view(
            template_name="authentication/login.html", redirect_authenticated_user=True
        ),
        name="login",
    ),
    path("signup/", authentication.views.signup, name="signup"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "change-password/",
        PasswordChangeView.as_view(
            template_name="authentication/password_change_form.html"
        ),
        name="password_change",
    ),
    path(
        "change-password-done/",
        PasswordChangeDoneView.as_view(
            template_name="authentication/password_change_done.html"
        ),
        name="password_change_done",
    ),
    path("flux/", bookreview.views.flux, name="flux"),
    path("follows/", bookreview.views.follows, name="follows"),
    path("posts/", bookreview.views.posts, name="posts"),
    path('follows/<int:follows_id>/delete', bookreview.views.follows_delete, name='follows_delete'),
    path('ticket/create', bookreview.views.create_ticket, name='create_ticket'),
    path('ticket/<int:ticket_id>/edit', bookreview.views.edit_ticket, name='edit_ticket'),
    path('ticket/<int:ticket_id>/delete', bookreview.views.delete_ticket, name='delete_ticket'),
    path('review/create', bookreview.views.create_review, name='create_review'),
    path('review/<int:review_id>/edit', bookreview.views.edit_review, name='edit_review'),
    path('review/ticket/<int:ticket_id>/create', bookreview.views.create_review_ticket, name='create_review_ticket'),
    path('review/<int:review_id>/delete', bookreview.views.delete_review, name='delete_review'),
]

# les images stockées dans le répertoire MEDIA_ROOT seront servies au chemin donné par MEDIA_URL
# Seulement en environnement de developpement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
