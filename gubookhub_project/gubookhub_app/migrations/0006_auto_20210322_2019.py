# Generated by Django 2.2.17 on 2021-03-22 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gubookhub_app', '0005_auto_20210322_1926'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='slug',
        ),
        migrations.AlterField(
            model_name='subject',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
