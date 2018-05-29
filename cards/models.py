import uuid
import os
from django.db import models
from accounts.models import User
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.utils.text import slugify


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('photos', filename)


class Rarity(models.Model):
    description = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.description

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.description)
        super().save(*args, **kwargs)


class Department(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    head = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def svg_template(self):
        return 'assets/logos/%s.svg' % (self.slug)


class Card(models.Model):
    is_badge = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    order_card = models.IntegerField()
    description = models.CharField(max_length=300)
    photo = models.ImageField(upload_to=get_file_path, null=True, blank=True)
    photo_thumbnail = ImageSpecField(
        source='photo',
        processors=[ResizeToFill(100, 50)],
        format='JPEG',
        options={'quality': 80}
    )
    fk_rarity = models.ForeignKey(Rarity, on_delete=models.CASCADE)
    fk_department = models.ForeignKey(Department, on_delete=models.CASCADE)
    wave = models.IntegerField(default=1)
    active = models.BooleanField(default=True)
    arrival_date = models.DateField()

    def __str__(self):
        return self.name + ' - ' + self.description

    def html_template(self):
        return 'cards/types/%s.html' % (self.fk_department.slug)


class Code(models.Model):
    code = models.CharField(max_length=200, unique=True)
    fk_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    fk_card = models.ForeignKey(Card, on_delete=models.CASCADE)

    def __str__(self):
        return self.code
