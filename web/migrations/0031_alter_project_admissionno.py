# Generated by Django 4.0.5 on 2022-06-29 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0030_project_admissionno'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='admissionNo',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
