from django import forms
from .models import UserFollows, Ticket, Review


class UserFollowsForm(forms.ModelForm):
    class Meta:
        model = UserFollows
        fields = ["followed_user"]
        labels = {
            "followed_user": "Choisir utilisateur",
        }


class TicketForm(forms.ModelForm):
    # champ caché
    edit_ticket = forms.BooleanField(
        widget=forms.HiddenInput, initial=True, required=False
    )

    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]


class DeleteTicketForm(forms.Form):
    # champ caché
    delete_ticket = forms.BooleanField(
        widget=forms.HiddenInput, initial=True, required=False
    )


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ["headline", "rating", "body"]

        widgets = {
            "rating": forms.RadioSelect(
                choices=[(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")]
            ),
        }
