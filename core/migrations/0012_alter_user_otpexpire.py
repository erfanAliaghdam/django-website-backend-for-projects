# Generated by Django 4.0.5 on 2022-06-27 19:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_user_otpcode_user_otpexpire_alter_user_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='otpExpire',
            field=models.DateTimeField(auto_now=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
