from django.contrib import admin
from bookreview.models import Ticket, Review, UserFollows

# Définition des classes d'administration personnalisées pour chaque modèle


class TicketAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "time_created", "id")


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("headline", "ticket", "rating", "user", "time_created", "id")


class UserFollowsAdmin(admin.ModelAdmin):
    list_display = ("user", "followed_user", "id")


# Enregistrement des classes d'administration personnalisées pour chaque modèle


admin.site.register(Ticket, TicketAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(UserFollows, UserFollowsAdmin)
