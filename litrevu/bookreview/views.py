from django.shortcuts import (
    render,
    redirect,
)  # Importation des fonctions de rendu et de redirection

from django.contrib.auth.decorators import (
    login_required,
)  # Décorateur pour vérifier si l'utilisateur est connecté

from django.http import (
    HttpResponseForbidden,
)  # Importation de la réponse HTTP pour les interdictions

from django.shortcuts import (
    get_object_or_404,
)  # Fonction pour obtenir un objet ou renvoyer une erreur 404

from django.contrib import messages  # Module pour gérer les messages flash

from django.utils import timezone  # Importation pour manipuler les dates et heures

from django.core.files.storage import (
    default_storage,
)  # Stockage par défaut pour gérer les fichiers

from django.db import (
    IntegrityError,
)  # Importation pour gérer les erreurs d'intégrité de la base de données

from .models import UserFollows, Ticket, Review
from .forms import UserFollowsForm, TicketForm, DeleteTicketForm, ReviewForm


# Ticket ---------------------------------------------------------------------


@login_required
def create_ticket(request):
    """
    Vue pour créer un nouveau ticket.

    Permet aux utilisateurs de créer un nouveau ticket. L'utilisateur doit être connecté.
    Après la création réussie du ticket, l'utilisateur est redirigé vers la page de flux.

    Args:
    request: Objet HttpRequest contenant les données de la requête HTTP.

    Returns:
    HttpResponse: Renvoie le rendu de la page de création de ticket avec le formulaire.

    """

    ticket_form = TicketForm()
    if request.method == "POST":
        ticket_form = TicketForm(request.POST, request.FILES)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            return redirect("flux")
        else:
            # Afficher les erreurs de validation du formulaire
            for field, errors in ticket_form.errors.items():
                for error in errors:
                    messages.error(request, f"Erreur dans le champ '{field}': {error}")

    context = {
        "ticket_form": ticket_form,
    }

    return render(request, "bookreview/create_ticket.html", context=context)


@login_required
def edit_ticket(request, ticket_id):
    """
    Vue pour éditer un ticket existant.

    Permet aux utilisateurs d'éditer un ticket existant. L'utilisateur doit être connecté.
    Après l'édition réussie du ticket, l'utilisateur est redirigé vers la page de flux.

    Args:
        request: Objet HttpRequest contenant les données de la requête HTTP.
        ticket_id: ID du ticket à éditer.

    Returns:
        HttpResponse: Renvoie le rendu de la page d'édition de ticket avec le formulaire.

    """

    ticket = get_object_or_404(Ticket, id=ticket_id)
    edit_form = TicketForm(instance=ticket)

    if request.method == "POST":

        edit_form = TicketForm(request.POST, request.FILES, instance=ticket)
        if edit_form.is_valid():
            ticket.time_created = timezone.now()
            edit_form.save()
            messages.success(
                request, f"Le Ticket {ticket.title} a été modifié avec succès."
            )
            return redirect("posts")
        else:
            # Afficher les erreurs de validation du formulaire
            for field, errors in edit_form.errors.items():
                for error in errors:
                    messages.error(request, f"Erreur dans le champ '{field}': {error}")

    context = {
        "edit_form": edit_form,
    }
    return render(request, "bookreview/edit_ticket.html", context=context)


@login_required
def delete_ticket(request, ticket_id):
    """
    Vue pour supprimer un ticket existant.

    Permet aux utilisateurs de supprimer un ticket existant. L'utilisateur doit être connecté.
    Après la suppression réussie du ticket, l'utilisateur est redirigé vers la page de flux.

    Args:
        request: Objet HttpRequest contenant les données de la requête HTTP.
        ticket_id: ID du ticket à supprimer.

    Returns:
        HttpResponse: Redirige vers la page de flux après la suppression réussie du ticket.

    """
    ticket = get_object_or_404(Ticket, id=ticket_id)

    # Vérifie que l'utilisateur est autorisé à supprimer l'objet
    if ticket.user != request.user:

        return HttpResponseForbidden(
            "Vous n'êtes pas autorisé à effectuer cette action."
        )

    try:
        # Supprimer le fichier image associé au ticket s'il existe
        if ticket.image:
            # Obtenir le chemin du fichier
            file_path = ticket.image.path
            # Supprimer le fichier
            default_storage.delete(file_path)

        ticket.delete()

        messages.success(
            request, f"Le Ticket {ticket.title} a été supprimé avec succès."
        )
    except IntegrityError as e:
        # Gérer les erreurs spécifiques liées à l'intégrité de la base de données
        messages.error(
            request,
            f"Une erreur d'intégrité de la base de données s'est produite : {e}",
        )
    except Exception as e:
        # Gérer les autres exceptions génériques
        messages.error(
            request,
            f"Une erreur s'est produite lors de la suppression de l'objet : {e}",
        )

    return redirect("posts")


# Review ---------------------------------------------------------------------


@login_required
def create_review(request):
    review_form = ReviewForm()
    ticket_form = TicketForm()
    if request.method == "POST":
        review_form = ReviewForm(request.POST)
        ticket_form = TicketForm(request.POST, request.FILES)
        if all([review_form.is_valid(), ticket_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect("flux")
        else:
            # Afficher les erreurs de validation du formulaire
            for field, errors in review_form.errors.items():
                for error in errors:
                    messages.error(request, f"Erreur dans le champ '{field}': {error}")

    context = {"review_form": review_form, "ticket_form": ticket_form}
    return render(request, "bookreview/create_review.html", context=context)


@login_required
def create_review_ticket(request, ticket_id):
    """
    Vue pour créer une nouvelle critique.

    Permet aux utilisateurs de créer une nouvelle critique pour un ticket. L'utilisateur doit être connecté.
    Si la critique et le ticket sont valides, ils sont enregistrés dans la base de données.
    Après la création réussie de la critique, l'utilisateur est redirigé vers la page de flux.

    Args:
        request: Objet HttpRequest contenant les données de la requête HTTP.

    Returns:
        HttpResponse: Renvoie le rendu de la page de création de critique avec le formulaire.

    """

    ticket = get_object_or_404(Ticket, id=ticket_id)
    review_form = ReviewForm()
    if request.method == "POST":
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect("flux")
        else:
            # Afficher les erreurs de validation du formulaire
            for field, errors in review_form.errors.items():
                for error in errors:
                    messages.error(request, f"Erreur dans le champ '{field}': {error}")

    context = {
        "ticket": ticket,
        "review_form": review_form,
    }
    return render(request, "bookreview/create_review_ticket.html", context=context)


@login_required
def edit_review(request, review_id):
    """
    Vue pour éditer une critique existante.

    Permet aux utilisateurs d'éditer une critique existante. L'utilisateur doit être connecté.
    Si la critique est valide, elle est mise à jour dans la base de données.
    Après l'édition réussie de la critique, l'utilisateur est redirigé vers la page de flux.

    Args:
        request: Objet HttpRequest contenant les données de la requête HTTP.
        review_id: ID de la critique à éditer.

    Returns:
        HttpResponse: Renvoie le rendu de la page d'édition de critique avec le formulaire.

    """

    review = get_object_or_404(Review, id=review_id)
    edit_form = ReviewForm(instance=review)
    ticket = review.ticket
    if request.method == "POST":
        edit_form = ReviewForm(request.POST, instance=review)
        if edit_form.is_valid():
            review.time_created = timezone.now()
            edit_form.save()
            messages.success(
                request, f"La Critique {review.ticket} a été modifié avec succès."
            )
            return redirect("posts")
        else:
            # Afficher les erreurs de validation du formulaire
            for field, errors in edit_form.errors.items():
                for error in errors:
                    messages.error(request, f"Erreur dans le champ '{field}': {error}")

    context = {
        "edit_form": edit_form,
        "ticket": ticket,
    }
    return render(request, "bookreview/edit_review.html", context=context)


@login_required
def delete_review(request, review_id):
    """
    Vue pour supprimer une critique existante.

    Permet aux utilisateurs de supprimer une critique existante. L'utilisateur doit être connecté.
    Après la suppression réussie de la critique, l'utilisateur est redirigé vers la page de flux.

    Args:
        request: Objet HttpRequest contenant les données de la requête HTTP.
        review_id: ID de la critique à supprimer.

    Returns:
        HttpResponse: Redirige vers la page de flux après la suppression réussie de la critique.

    """
    review = get_object_or_404(Review, id=review_id)

    if review.user != request.user:
        return HttpResponseForbidden(
            "Vous n'êtes pas autorisé à effectuer cette action."
        )

    try:
        review.delete()
        messages.success(
            request, f"La Critique {review.ticket} a été supprimé avec succès."
        )
    except IntegrityError as e:
        # Gérer les erreurs spécifiques liées à l'intégrité de la base de données
        messages.error(
            request,
            f"Une erreur d'intégrité de la base de données s'est produite : {e}",
        )
    except Exception as e:
        # Gérer les autres exceptions génériques
        messages.error(
            request,
            f"Une erreur s'est produite lors de la suppression de l'objet : {e}",
        )

    return redirect("posts")


# Follows users  ---------------------------------------------------------------------


@login_required
def follows(request):
    """
    Vue pour afficher les abonnements et les abonnés d'un utilisateur.

    Permet à l'utilisateur de voir la liste des utilisateurs qu'il suit et des utilisateurs qui le suivent.
    L'utilisateur doit être connecté pour accéder à cette vue.
    Il peut également ajouter de nouveaux abonnements en soumettant un formulaire.
    Si un utilisateur est déjà suivi, un message d'erreur approprié est affiché.

    Args:
        request: Objet HttpRequest contenant les données de la requête HTTP.

    Returns:
        HttpResponse: Renvoie le rendu de la page d'affichage des abonnements et abonnés.

    """

    # Récupérer les utilisateurs suivis et les abonnés de l'utilisateur connecté
    followings = UserFollows.objects.filter(user=request.user)
    followers = UserFollows.objects.filter(followed_user=request.user)

    if request.method == "POST":
        form = UserFollowsForm(request.POST)
        if form.is_valid():
            try:
                user_follow = form.save(commit=False)
                user_follow.user = request.user
                user_follow.save()
            except IntegrityError:
                messages.error(
                    request,
                    f"L'utilisateur {user_follow.followed_user} est deja dans votre liste de suivis",
                )
                return render(
                    request,
                    "bookreview/follows.html",
                    {"form": form, "followings": followings, "followers": followers},
                )

            return redirect("follows")
    else:
        form = UserFollowsForm()

    context = {
        "form": form,
        "followings": followings,
        "followers": followers,
    }

    return render(request, "bookreview/follows.html", context=context)


@login_required
def follows_delete(request, follows_id):
    """
    Vue pour supprimer un abonnement d'un utilisateur.

    Permet à l'utilisateur de supprimer un abonnement existant. L'utilisateur doit être connecté.
    Après la suppression réussie de l'abonnement, l'utilisateur est redirigé vers la page d'affichage des abonnements
    et abonnés.

    Args:
        request: Objet HttpRequest contenant les données de la requête HTTP.
        follows_id: ID de l'abonnement à supprimer.

    Returns:
        HttpResponse: Redirige vers la page d'affichage des abonnements et abonnés après la suppression réussie
        de l'abonnement.

    """

    follow = get_object_or_404(UserFollows, id=follows_id)

    # Vérifie que l'utilisateur est autorisé à supprimer l'objet
    if follow.user != request.user:

        return HttpResponseForbidden(
            "Vous n'êtes pas autorisé à effectuer cette action."
        )

    try:
        follow.delete()
        messages.success(request, f"{follow.followed_user} a été supprimé avec succès.")
    except IntegrityError as e:
        # Gérer les erreurs spécifiques liées à l'intégrité de la base de données
        messages.error(
            request,
            f"Une erreur d'intégrité de la base de données s'est produite : {e}",
        )
    except Exception as e:
        # Gérer les autres exceptions génériques
        messages.error(
            request,
            f"Une erreur s'est produite lors de la suppression de l'objet : {e}",
        )

    return redirect("follows")


# Posts ---------------------------------------------------------------------


@login_required
def posts(request):
    """
    Vue pour afficher la liste de tous les tickets et reviews de l'utilisateur connecté.

    Permet à l'utilisateur de voir tous les tickets et reviews qu'il a créés.
    L'utilisateur doit être connecté pour accéder à cette vue.
    Les posts sont triés par ordre antéchronologique de leur date de création.
    L'utilisateur peut lancer une modification ou une suppression de ses posts.

    Args:
        request: Objet HttpRequest contenant les données de la requête HTTP.

    Returns:
        HttpResponse: Renvoie le rendu de la page d'affichage des posts de l'utilisateur.
    """

    tickets = Ticket.objects.filter(user=request.user)
    reviews = Review.objects.filter(user=request.user)
    posts = list(tickets) + list(reviews)

    # Trier les posts par ordre antéchronologique
    posts.sort(key=lambda x: x.time_created, reverse=True)

    delete_form_ticket = DeleteTicketForm()

    context = {
        "posts": posts,
        "delete_form_ticket": delete_form_ticket,
    }

    return render(request, "bookreview/posts.html", context)


# Flux ---------------------------------------------------------------------


@login_required
def flux(request):
    """
    Vue pour afficher le flux d'activités de l'utilisateur connecté.

    Affiche les posts de l'utilisateur connecté, des utilisateurs qu'il suit et
    de toutes les réponses à ses tickets.
    Les posts sont triés par ordre antéchronologique de leur date de création.

    Args:
        request: Objet HttpRequest contenant les données de la requête HTTP.

    Returns:
        HttpResponse: Renvoie le rendu de la page d'affichage du flux d'activités.
    """

    # récupération des posts de l'utilsateur connecté
    tickets = Ticket.objects.filter(user=request.user)
    reviews = Review.objects.filter(user=request.user)

    # Utilisation d'un ensemble pour éviter les doublons
    posts_set = set(tickets) | set(reviews)

    # récupération des posts des followers
    follows = UserFollows.objects.filter(user=request.user)
    for follow in follows:
        tickets_followed = Ticket.objects.filter(user=follow.followed_user)
        reviews_followed = Review.objects.filter(user=follow.followed_user)
        posts_set |= set(tickets_followed) | set(reviews_followed)

    # récupération des reponses aux tickets de l'utilisateur connecté
    user_reviews = Review.objects.filter(ticket__user=request.user)
    posts_set |= set(user_reviews)

    # Trier les posts par ordre antéchronologique
    posts = sorted(posts_set, key=lambda x: x.time_created, reverse=True)

    context = {
        "posts": posts,
    }

    return render(request, "bookreview/flux.html", context)
