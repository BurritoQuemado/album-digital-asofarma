# Generated by Django 2.0.5 on 2018-06-05 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0004_auto_20180605_1648'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='receiver_read',
            field=models.BooleanField(default=False),
        ),
    ]