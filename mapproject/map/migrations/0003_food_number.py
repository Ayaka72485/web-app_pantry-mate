# Generated by Django 3.2 on 2024-06-05 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0002_auto_20240601_0543'),
    ]

    operations = [
        migrations.AddField(
            model_name='food',
            name='number',
            field=models.IntegerField(default=0),
        ),
    ]
