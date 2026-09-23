from django.contrib import admin
from .models import Building
from .models import Favorite

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'location', 'price')
    search_fields = ('title', 'location')

admin.site.register(Building)