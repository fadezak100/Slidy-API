# Generated by Django 4.1.5 on 2023-02-01 13:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('slides', '0012_remove_slide_users_slide_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='slide',
            name='user',
        ),
    ]