# Generated by Django 4.0.6 on 2022-07-07 07:14

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('web', '0042_requestitem_approved_time_requestitem_created_at_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='requestedprojects',
            options={'verbose_name': 'grouped requests by user request', 'verbose_name_plural': 'grouped requests by user request'},
        ),
        migrations.AlterUniqueTogether(
            name='requestedprojects',
            unique_together={('user', 'id')},
        ),
    ]
