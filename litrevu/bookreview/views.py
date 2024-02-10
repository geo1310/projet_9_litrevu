from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.db import IntegrityError
from .models import UserFollows
from .forms import UserFollowsForm


@login_required
def posts(request):
    return render(request, 'bookreview/posts.html')


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
            except IntegrityError as e:
                unique_error_message = str(e)
                form.add_error(None, unique_error_message)  # Ajouter l'erreur au formulaire
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
def flux(request):
    return render(request, 'bookreview/flux.html')
