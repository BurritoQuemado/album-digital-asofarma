# import math
from django.contrib.admin import SimpleListFilter
from django.contrib import admin
from .models import Card, Department, Rarity, Code
from import_export import fields, resources
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget
# from imagekit.admin import AdminThumbnail
from imagekit import ImageSpec
from imagekit.processors import ResizeToFill
from imagekit.cachefiles import ImageCacheFile
from django.db.models import Count


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


class HasPhotoFilter(SimpleListFilter):
    title = 'tiene foto'
    parameter_name = 'photo'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('no_photo', 'No tiene foto'),
            ('has_photo', 'Tiene foto'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'no_photo':
            return queryset.filter(photo='')
        if self.value() == 'has_photo':
            return queryset.all().exclude(photo='')


@admin.register(Card)
class CardAdmin(ImportExportModelAdmin):
    list_display = ('name', 'codes_count', 'id', 'order', 'fk_rarity', 'fk_department', 'wave', 'is_badge', 'active', 'page', )
    list_filter = ('active', HasPhotoFilter, 'wave', 'is_badge', 'fk_department', 'fk_rarity', )
    fields = ('photo', 'active', 'fk_department', 'fk_rarity', 'wave',)
    resource_class = CardResource
    # admin_thumbnail = AdminThumbnail(image_field=cached_admin_thumb)

    def queryset(self, request):
        qs = super(CardAdmin, self).queryset(request)
        qs = qs.annotate(codes_count=Count('code'))
        return qs

    def codes_count(self, obj):
        codes = Code.objects.filter(fk_card=obj).count()
        return codes
    # codes_count.short_description = 'Códigos'
    # codes_count.admin_order_field = 'codes_count'

    def import_action(self, request, *args, **kwargs):
        response = super().import_action(request, *args, **kwargs)
        # departments = Department.objects.all().order_by('id')
        # cards_order = 1
        # for department in departments:
        #     cards = Card.objects.filter(fk_department=department, active=True).order_by('id')
        #     for index, card in enumerate(cards):
        #         card.page = 1 if index is 0 else int(math.ceil(index / 12))
        #         card.order = cards_order
        #         card.save()
        #         cards_order += 1
        return response


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug',)
    fields = ('name', 'description', 'head',)


@admin.register(Rarity)
class RarityAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'slug',)
    fields = ('description',)
