# Generated by Django 2.0.5 on 2018-07-09 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20180709_1057'),
    ]

    operations = [
        migrations.CreateModel(
            name='Options',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('is_correct', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('options', models.ManyToManyField(to='events.Options')),
            ],
        ),
        migrations.RemoveField(
            model_name='trivia',
            name='question_one',
        ),
        migrations.RemoveField(
            model_name='trivia',
            name='question_three',
        ),
        migrations.RemoveField(
            model_name='trivia',
            name='question_two',
        ),
        migrations.AddField(
            model_name='trivia',
            name='questions',
            field=models.ManyToManyField(to='events.Question'),
        ),
    ]
