from django import forms
from .models import UserFollows, Ticket


class UserFollowsForm(forms.ModelForm):
    class Meta:
        model = UserFollows
        fields = ['followed_user']


class TicketForm(forms.ModelForm):
    # champ caché
    edit_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True, required=False)

    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']


class DeleteTicketForm(forms.Form):
    # champ caché
    delete_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True, required=False)
