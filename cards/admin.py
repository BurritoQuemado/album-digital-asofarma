import math
from django.contrib import admin
from .models import Card, Department, Rarity
from import_export import fields, resources
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget
from imagekit.admin import AdminThumbnail
from imagekit import ImageSpec
from imagekit.processors import ResizeToFill
from imagekit.cachefiles import ImageCacheFile


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
        fields = ('id', 'order', 'fk_rarity', 'name', 'fk_department', 'description', 'arrival_date', 'is_badge', 'active', 'wave',)


class AdminThumbnailSpec(ImageSpec):
    processors = [ResizeToFill(120, 149)]
    format = 'JPEG'
    options = {'quality': 60}


def cached_admin_thumb(instance):
    if instance.photo:
        cached = ImageCacheFile(AdminThumbnailSpec(instance.photo))
        cached.generate()
        return cached
    return None


@admin.register(Card)
class CardAdmin(ImportExportModelAdmin):
    list_display = ('name', 'admin_thumbnail', 'id', 'order', 'fk_rarity', 'fk_department', 'wave', 'is_badge', 'active', 'page', )
    list_filter = ('wave', 'is_badge', 'fk_department', 'fk_rarity', 'active',)
    fields = ('photo', 'active', 'fk_department', 'fk_rarity', 'wave',)
    resource_class = CardResource
    admin_thumbnail = AdminThumbnail(image_field=cached_admin_thumb)

    def import_action(self, request, *args, **kwargs):
        response = super().import_action(request, *args, **kwargs)
        departments = Department.objects.all().order_by('id')
        cards_order = 1
        for department in departments:
            cards = Card.objects.filter(fk_department=department, active=True).order_by('id')
            for index, card in enumerate(cards):
                card.page = 1 if index is 0 else int(math.ceil(index / 12))
                card.order = cards_order
                card.save()
                cards_order += 1
        return response


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug',)
    fields = ('name', 'description', 'head',)


@admin.register(Rarity)
class RarityAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'slug',)
    fields = ('description',)
