from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.contrib import messages

from django.db import IntegrityError
from .models import UserFollows, Ticket, Review
from .forms import UserFollowsForm, TicketForm, DeleteTicketForm, ReviewForm


# Ticket


@login_required
def create_ticket(request):

    ''' Création d'un Ticket '''

    ticket_form = TicketForm()
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            return redirect('flux')
        else:
            # Afficher les erreurs de validation du formulaire
            for field, errors in ticket_form.errors.items():
                for error in errors:
                    messages.error(request, f"Erreur dans le champ '{field}': {error}")

    context = {
        'ticket_form': ticket_form,
    }

    return render(request, 'bookreview/create_ticket.html', context=context)


@login_required
def edit_ticket(request, ticket_id):

    ''' Edition d'un Ticket '''

    ticket = get_object_or_404(Ticket, id=ticket_id)
    edit_form = TicketForm(instance=ticket)
    delete_form = DeleteTicketForm()
    if request.method == 'POST':
        if 'edit_ticket' in request.POST:
            edit_form = TicketForm(request.POST, request.FILES, instance=ticket)
            if edit_form.is_valid():
                edit_form.save()

                return redirect('flux')
            else:
                # Afficher les erreurs de validation du formulaire
                for field, errors in edit_form.errors.items():
                    for error in errors:
                        messages.error(request, f"Erreur dans le champ '{field}': {error}")

        if 'delete_ticket' in request.POST:
            delete_form = DeleteTicketForm(request.POST)
            if delete_form.is_valid():
                ticket.delete()
                return redirect('flux')
    context = {
        'edit_form': edit_form,
        'delete_form': delete_form,
    }
    return render(request, 'bookreview/edit_ticket.html', context=context)


# Review


@login_required
def create_review(request, ticket_id):

    ''' Creation d'une Critique '''

    ticket = get_object_or_404(Ticket, id=ticket_id)
    review_form = ReviewForm()
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('flux')
        else:
            # Afficher les erreurs de validation du formulaire
            for field, errors in review_form.errors.items():
                for error in errors:
                    messages.error(request, f"Erreur dans le champ '{field}': {error}")

    context = {
        'ticket': ticket,
        'review_form': review_form,
    }
    return render(request, 'bookreview/create_review.html', context=context)


@login_required
def edit_review(request, review_id):

    ''' Edition d'une Critique '''

    review = get_object_or_404(Review, id=review_id)
    edit_form = ReviewForm(instance=review)
    ticket = review.ticket
    if request.method == 'POST':
        edit_form = ReviewForm(request.POST, instance=review)
        if edit_form.is_valid():
            edit_form.save()

            return redirect('flux')
        else:
            # Afficher les erreurs de validation du formulaire
            for field, errors in edit_form.errors.items():
                for error in errors:
                    messages.error(request, f"Erreur dans le champ '{field}': {error}")

    context = {
        'edit_form': edit_form,
        'ticket': ticket,
    }
    return render(request, 'bookreview/edit_review.html', context=context)


# Follow users


@login_required
def follows(request):

    '''Abonnements et abonés d'un utilisateur'''

    # Récupérer les utilisateurs suivis et les abonnés de l'utilisateur connecté
    followings = UserFollows.objects.filter(user=request.user)
    followers = UserFollows.objects.filter(followed_user=request.user)

    if request.method == 'POST':
        form = UserFollowsForm(request.POST)
        if form.is_valid():
            try:
                user_follow = form.save(commit=False)
                user_follow.user = request.user
                user_follow.save()
            except IntegrityError:
                messages.error(request, f"L'utilisateur {user_follow.followed_user} est deja dans votre liste de suivis")
                return render(request, 'bookreview/follows.html', {'form': form, 'followings': followings, 'followers': followers})

            return redirect('follows')
    else:
        form = UserFollowsForm()

    context = {
        'form': form,
        'followings': followings,
        'followers': followers,
    }

    return render(request, 'bookreview/follows.html', context=context)


@login_required
def follows_delete(request, follows_id):

    ''' Suppression des abonnements d'un utilisateur '''
    
    follow = get_object_or_404(UserFollows, id=follows_id)

    # Vérifie que l'utilisateur est autorisé à supprimer l'objet
    if follow.user != request.user:

        return HttpResponseForbidden("Vous n'êtes pas autorisé à effectuer cette action.")

    try:
        follow.delete()
        messages.success(request, f"{follow.followed_user} a été supprimé avec succès.")
    except IntegrityError as e:
        # Gérer les erreurs spécifiques liées à l'intégrité de la base de données
        messages.error(request, f"Une erreur d'intégrité de la base de données s'est produite : {e}")
    except Exception as e:
        # Gérer les autres exceptions génériques
        messages.error(request, f"Une erreur s'est produite lors de la suppression de l'objet : {e}")

    return redirect('follows')


# Posts


@login_required
def posts(request):

    return render(request, 'bookreview/posts.html')


# Flux


@login_required
def flux(request):

    return render(request, 'bookreview/flux.html')
