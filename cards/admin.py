from django.contrib import admin
from .models import Card, Department, Rarity
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class CardResource(resources.ModelResource):

    class Meta:
        model = Card
        fields = ('id', 'order_card', 'fk_rarity__description', 'name', 'fk_department__name', 'description', 'arrival_date', 'is_badge', 'active', 'wave',)


# @admin.register(Department)
# class DepartmentAdmin(ImportExportModelAdmin):
#     list_display = ('id', 'name', 'fk_rarity', 'fk_department', 'wave', 'is_badge')
#     list_filter = ('wave', 'is_badge', 'fk_department', 'fk_rarity',)


# @admin.register(Rarity)
# class RarityAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'fk_rarity', 'fk_department', 'wave', 'is_badge')
#     list_filter = ('wave', 'is_badge', 'fk_department', 'fk_rarity',)
