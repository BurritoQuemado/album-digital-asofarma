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

    class Meta:
        verbose_name = 'Rareza'
        verbose_name_plural = 'Rarezas'

    description = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.description

    def save(self, *args, **kwargs):
        self.slug = slugify(self.description)
        super().save(*args, **kwargs)


class Department(models.Model):

    class Meta:
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    head = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def svg_template(self):
        return 'assets/logos/%s.svg' % (self.slug)


class Card(models.Model):

    class Meta:
        verbose_name = 'Carta'
        verbose_name_plural = 'Cartas'

    is_badge = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    order = models.IntegerField(default=0, null=True, blank=True)
    description = models.CharField(max_length=300, default='No info')
    charge = models.CharField(max_length=100, default='No info')
    photo = models.ImageField(upload_to=get_file_path, null=True, blank=True)
    photo_thumbnail = ImageSpecField(
        source='photo',
        processors=[ResizeToFill(450, 560)],
        format='JPEG',
        options={'quality': 80}
    )
    fk_rarity = models.ForeignKey(Rarity, on_delete=models.CASCADE)
    fk_department = models.ForeignKey(Department, on_delete=models.CASCADE)
    wave = models.IntegerField(default=1)
    active = models.BooleanField(default=True)
    arrival_date = models.CharField(max_length=4)
    birth_date = models.CharField(max_length=100, default='No info')
    true_department = models.CharField(max_length=100, default='No info')
    page = models.IntegerField(default=1)

    def __str__(self):
        return self.name + ' - ' + self.description

    def html_template(self):
        return 'cards/types/%s.html' % (self.fk_department.slug)

    def img_template(self):
        return 'assets/badges/%s.png' % (self.fk_department.slug)



class Code(models.Model):

    class Meta:
        verbose_name = 'Código'
        verbose_name_plural = 'Códigos'

    code = models.CharField(max_length=200, unique=True)
    fk_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='code')
    fk_card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='card_code')

    def __str__(self):
        return self.code


class Notification(models.Model):

    class Meta:
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'

    sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='receiver', on_delete=models.CASCADE)
    code = models. ForeignKey(Code, on_delete=models.CASCADE)
    sender_read = models.BooleanField(default=False)
    receiver_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
