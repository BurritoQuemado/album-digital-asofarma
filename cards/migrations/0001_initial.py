# Generated by Django 2.0.4 on 2018-05-16 21:52

import cards.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('order', models.IntegerField()),
                ('description', models.CharField(max_length=300)),
                ('photo', models.ImageField(blank=True, null=True, upload_to=cards.models.get_file_path)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Code',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=200, unique=True)),
                ('fk_card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cards.Card')),
                ('fk_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Rarity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='card',
            name='fk_department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cards.Department'),
        ),
        migrations.AddField(
            model_name='card',
            name='fk_rarity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cards.Rarity'),
        ),
    ]
