from django.contrib import admin
from .models import User, Player, Room, Submission, Result

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email')

class PlayerAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'status')


class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'creator', 'date_created', 'active')

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'player', 'room', 'categories', 'price', 'parking', 'outdoor')

class ResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'room', 'restraunt_name', 'display_phone', 'yelp_url', 'rating')

admin.site.register(User, UserAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(Result, ResultAdmin)