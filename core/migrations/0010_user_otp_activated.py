# Generated by Django 4.0.5 on 2022-06-27 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_alter_user_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='otp_activated',
            field=models.BooleanField(default=False),
        ),
    ]
