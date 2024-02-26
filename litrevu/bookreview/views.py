from PIL import Image
from io import BytesIO
from django.core.files import File

from django.contrib import messages  # Module pour gérer les messages flash
from django.contrib.auth.decorators import (
    login_required,
)  # Décorateur pour vérifier si l'utilisateur est connecté
from django.core.files.storage import (
    default_storage,
)  # Stockage par défaut pour gérer les fichiers
from django.db import (
    IntegrityError,
)  # Importation pour gérer les erreurs d'intégrité de la base de données
from django.http import (
    HttpResponseForbidden,
)  # Importation de la réponse HTTP pour les interdictions
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import DeleteTicketForm, ReviewForm, TicketForm, UserFollowsForm
from .models import Review, Ticket, UserFollows

COMMON_IMPORTS = {
    "unauthorized_msg": "Vous n'êtes pas autorisé à effectuer cette action.",
}


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
        image_file = request.FILES["image"]

        if ticket_form.is_valid():

            ticket = ticket_form.save(commit=False)
            ticket.user = request.user

            # Modifie l'image

            try:
                image_buffer_modify, webp_path = compress_image(image_file)
                # Enregistrer l'image compressée en buffer dans le champ ImageField du modèle Ticket
                ticket.image.save(webp_path, File(image_buffer_modify), save=False)
                image_buffer_modify.close()

            except Exception:
                messages.error(
                    request,
                    "Une erreur s'est produite lors de la compression de l'image.",
                )

            ticket.save()

            return redirect("flux")

        else:
            # Affiche les erreurs de validation du formulaire
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

    # image d'origine
    old_image_path = ticket.image.path

    edit_form = TicketForm(request.POST or None, request.FILES or None, instance=ticket)

    if request.method == "POST" and edit_form.is_valid():

        # Vérifie si une nouvelle image a été fournie, la modifie  et supprime l ancienne si elle existe
        if "image" in request.FILES:

            image_file = request.FILES["image"]

            # Modifie l'image
            try:
                image_buffer_modify, webp_path = compress_image(image_file)

                # Enregistre l'image compressée en tampon dans le champ ImageField du modèle Ticket
                ticket.image.save(webp_path, File(image_buffer_modify), save=False)
                image_buffer_modify.close()

            except Exception:
                messages.error(
                    request,
                    "Une erreur s'est produite lors de la compression de l'image.",
                )

            # supprime l'ancienne image
            default_storage.delete(old_image_path)

        ticket.time_created = timezone.now()
        ticket.save()

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

        return HttpResponseForbidden(COMMON_IMPORTS["unauthorized_msg"])

    try:
        # Supprime le fichier image associé au ticket s'il existe
        if ticket.image:

            file_path = ticket.image.path
            default_storage.delete(file_path)

        ticket.delete()

        messages.success(
            request, f"Le Ticket {ticket.title} a été supprimé avec succès."
        )

    except IntegrityError as e:
        # Gére les erreurs spécifiques liées à l'intégrité de la base de données
        messages.error(
            request,
            f"Une erreur d'intégrité de la base de données s'est produite : {e}",
        )

    except Exception as e:
        # Gére les autres exceptions génériques
        messages.error(
            request,
            f"Une erreur s'est produite lors de la suppression de l'objet : {e}",
        )

    return redirect("posts")


# Review ---------------------------------------------------------------------


@login_required
def create_review(request):
    """
    Crée une nouvelle critique.

    Cette vue permet aux utilisateurs connectés de créer une nouvelle critique.
    Si une méthode POST est utilisée, les données du formulaire sont validées.
    Si les formulaires de critique et de ticket sont valides, une nouvelle critique
    est créée et associée à un nouveau ticket, puis l'utilisateur est redirigé
    vers la page de flux.

    Args:
        request (HttpRequest): L'objet HttpRequest contenant les données de la requête HTTP.

    Returns:
        HttpResponse: Renvoie le rendu de la page de création de critique avec les formulaires.

    """

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
            # Affiche les erreurs de validation du formulaire
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
            # Affiche les erreurs de validation du formulaire
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
            # Affiche les erreurs de validation du formulaire
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
        return HttpResponseForbidden(COMMON_IMPORTS["unauthorized_msg"])

    try:
        review.delete()
        messages.success(
            request, f"La Critique {review.ticket} a été supprimé avec succès."
        )

    except IntegrityError as e:
        # Gére les erreurs spécifiques liées à l'intégrité de la base de données
        messages.error(
            request,
            f"Une erreur d'intégrité de la base de données s'est produite : {e}",
        )

    except Exception as e:
        # Gére les autres exceptions génériques
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

        return HttpResponseForbidden(COMMON_IMPORTS["unauthorized_msg"])

    try:
        follow.delete()
        messages.success(request, f"{follow.followed_user} a été supprimé avec succès.")

    except IntegrityError as e:
        # Gére les erreurs spécifiques liées à l'intégrité de la base de données
        messages.error(
            request,
            f"Une erreur d'intégrité de la base de données s'est produite : {e}",
        )

    except Exception as e:
        # Gére les autres exceptions génériques
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

    # récupération des posts des followeds
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


# Fonctions diverses ---------------------------------------------------------------------


def compress_image(image_file):
    """
    Convertit une image en format WEBP et retourne les données de l'image compressée ainsi que le chemin du fichier.

    Args:
        image_file (UploadedFile): Objet de fichier de l'image à compresser.

    Returns:
        tuple: Un tuple contenant les données de l'image compressée (BytesIO) et le chemin du fichier WEBP.

        - image_buffer (BytesIO): Les données de l'image compressée.
        - webp_file_path (str): Le chemin du fichier WEBP.
    """

    # parametres de modifications des images
    size_img = (500, 500)
    quality_img = 70
    format_img = "WEBP"

    try:
        # Ouvrir l'image avec Pillow
        with Image.open(image_file) as img:

            # Redimensionnement en gardant les proportions
            img.thumbnail(size_img)

            # Enregistrer l'image compressée en mémoire tampon
            image_buffer = BytesIO()
            img.save(image_buffer, format=format_img, quality=quality_img)
            # déplace le pointeur de lecture au début deu tampon
            image_buffer.seek(0)

        # Créer le chemin de fichier avec l'extension .webp
        webp_file_path = f"{image_file.name.split('.')[0]}.webp"

    except Exception as e:
        print(20 * "-")
        print(f"Une erreur s'est produite lors de la compression de l'image : {e}")
        print(20 * "-")
        return None, None

    return image_buffer, webp_file_path
