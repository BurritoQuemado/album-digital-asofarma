from django.contrib import admin
from .models import Card


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'fk_rarity', 'fk_department', 'wave', 'is_badge')
    list_filter = ('wave', 'is_badge', 'fk_department', 'fk_rarity',)
