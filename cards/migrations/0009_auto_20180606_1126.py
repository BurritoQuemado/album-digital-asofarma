# Generated by Django 2.0.5 on 2018-06-06 16:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0008_card_page'),
    ]

    operations = [
        migrations.RenameField(
            model_name='card',
            old_name='order_card',
            new_name='order',
        ),
    ]