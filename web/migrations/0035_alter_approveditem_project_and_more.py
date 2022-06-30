# Generated by Django 4.0.5 on 2022-06-30 10:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('web', '0034_approveditem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='approveditem',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='approved_projects', to='web.project'),
        ),
        migrations.AlterField(
            model_name='approvedrequest',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='approved_projects', to=settings.AUTH_USER_MODEL),
        ),
    ]
