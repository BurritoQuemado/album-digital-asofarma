from django.contrib import admin
from .models import Card, Department, Rarity
from import_export import fields, resources
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget


class CardResource(resources.ModelResource):
    fk_department = fields.Field(
        column_name='fk_department',
        attribute='fk_department',
        widget=ForeignKeyWidget(Department, 'name'))
    fk_rarity = fields.Field(
        column_name='fk_rarity',
        attribute='fk_rarity',
        widget=ForeignKeyWidget(Rarity, 'description'))

    class Meta:
        model = Card
        fields = ('id', 'order_card', 'fk_rarity', 'name', 'fk_department', 'description', 'arrival_date', 'is_badge', 'active', 'wave',)


@admin.register(Card)
class CardAdmin(ImportExportModelAdmin):
    list_display = ('name', 'id', 'fk_rarity', 'fk_department', 'wave', 'is_badge', 'active',)
    list_filter = ('wave', 'is_badge', 'fk_department', 'fk_rarity', 'active',)
    fields = ('photo', 'active', 'fk_department', 'fk_rarity', 'wave',)
    resource_class = CardResource


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug',)
    fields = ('name', 'description', 'head',)


@admin.register(Rarity)
class RarityAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'slug',)
    fields = ('description',)
