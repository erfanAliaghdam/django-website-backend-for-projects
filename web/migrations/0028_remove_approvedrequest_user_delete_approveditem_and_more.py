# Generated by Django 4.0.5 on 2022-06-29 12:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0027_alter_profilestud_major_alter_profilestud_resume'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='approvedrequest',
            name='user',
        ),
        migrations.DeleteModel(
            name='ApprovedItem',
        ),
        migrations.DeleteModel(
            name='ApprovedRequest',
        ),
    ]
