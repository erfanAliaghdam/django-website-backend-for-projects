# Generated by Django 4.0.5 on 2022-06-29 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_alter_user_otpexpire'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='resume',
            field=models.TextField(blank=True),
        ),
    ]
