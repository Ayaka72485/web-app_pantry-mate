# Generated by Django 5.1.1 on 2024-10-22 06:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0008_food_template'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='food_template',
            name='number',
        ),
        migrations.RemoveField(
            model_name='food_template',
            name='unit',
        ),
    ]
