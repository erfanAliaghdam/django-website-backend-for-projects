# Generated by Django 4.0.5 on 2022-06-29 12:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0028_remove_approvedrequest_user_delete_approveditem_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profilestud',
            name='resume',
        ),
    ]
