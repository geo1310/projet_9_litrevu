from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.contrib import messages

from django.db import IntegrityError
from .models import UserFollows
from .forms import UserFollowsForm, TicketForm


@login_required
def posts(request):

    return render(request, 'bookreview/posts.html')


@login_required
def ticket_create(request):
    ticket_form = TicketForm()
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        if ticket_form.is_valid():
            print('sauvegarde du ticket')
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            return redirect('flux')
        else:
            # Afficher les erreurs de validation du formulaire
            messages.error(request, "Il y a des erreurs dans le formulaire.")
    context = {
        'ticket_form': ticket_form,
    }

    return render(request, 'bookreview/ticket.html', context=context)


@login_required
def follows(request):
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
    # Vérifier que l'utilisateur est autorisé à supprimer l'objet
    follow = get_object_or_404(UserFollows, id=follows_id)
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


@login_required
def flux(request):
    
    return render(request, 'bookreview/flux.html')
