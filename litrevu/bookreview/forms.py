from django import forms
from .models import UserFollows


class UserFollowsForm(forms.ModelForm):
    class Meta:
        model = UserFollows
        fields = ['followed_user']