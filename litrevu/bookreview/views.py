from django.shortcuts import render

from django.contrib.auth.decorators import login_required


@login_required
def posts(request):
    return render(request, 'bookreview/posts.html')


@login_required
def follows(request):
    return render(request, 'bookreview/follows.html')


@login_required
def flux(request):
    return render(request, 'bookreview/flux.html')
