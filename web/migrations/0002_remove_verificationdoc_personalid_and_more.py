# Generated by Django 4.0.5 on 2022-06-12 06:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='verificationdoc',
            name='personalId',
        ),
        migrations.RemoveField(
            model_name='verificationdoc',
            name='professor',
        ),
        migrations.AddField(
            model_name='verificationdoc',
            name='document',
            field=models.FileField(default=1, upload_to=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='verificationdoc',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='VerificationDocument',
        ),
    ]
