# Generated by Django 3.0 on 2021-10-23 12:44

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0002_auto_20211023_1236'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Content',
            new_name='Feed',
        ),
    ]
