# Generated by Django 2.1.3 on 2021-07-09 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0011_auto_20180709_1827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='order',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
