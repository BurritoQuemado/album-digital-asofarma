# Generated by Django 2.2 on 2021-07-12 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("cards", "0012_auto_20210709_1354")]

    operations = [
        migrations.AddField(
            model_name="card",
            name="birth_date",
            field=models.CharField(default="No info", max_length=100),
        ),
        migrations.AddField(
            model_name="card",
            name="charge",
            field=models.CharField(default="No info", max_length=100),
        ),
        migrations.AddField(
            model_name="card",
            name="true_department",
            field=models.CharField(default="No info", max_length=100),
        ),
        migrations.AlterField(
            model_name="card", name="arrival_date", field=models.CharField(max_length=4)
        ),
        migrations.AlterField(
            model_name="card",
            name="description",
            field=models.CharField(default="No info", max_length=300),
        ),
    ]
