# Generated by Django 4.1.5 on 2023-02-01 13:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_remove_user_slides_user_slides'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='slides',
        ),
    ]