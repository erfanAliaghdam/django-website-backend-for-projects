# Generated by Django 4.0.5 on 2022-07-03 11:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0038_messageforadmission_remove_approvedrequest_user_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MessageForAdmission',
        ),
    ]
