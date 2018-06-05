# Generated by Django 2.0.5 on 2018-06-05 21:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0003_notification'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='card',
            options={'verbose_name': 'Carta', 'verbose_name_plural': 'Cartas'},
        ),
        migrations.AlterModelOptions(
            name='code',
            options={'verbose_name': 'Código', 'verbose_name_plural': 'Códigos'},
        ),
        migrations.AlterModelOptions(
            name='department',
            options={'verbose_name': 'Departamento', 'verbose_name_plural': 'Departamentos'},
        ),
        migrations.AlterModelOptions(
            name='rarity',
            options={'verbose_name': 'Rareza', 'verbose_name_plural': 'Rarezas'},
        ),
        migrations.RenameField(
            model_name='notification',
            old_name='read',
            new_name='sender_read',
        ),
    ]
