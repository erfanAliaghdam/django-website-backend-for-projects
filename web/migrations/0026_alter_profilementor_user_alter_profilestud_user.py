# Generated by Django 4.0.5 on 2022-06-26 11:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('web', '0025_alter_verificationdoc_document'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilementor',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile_mentor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='profilestud',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile_stud', to=settings.AUTH_USER_MODEL),
        ),
    ]
