# Generated by Django 4.0.5 on 2022-06-13 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0010_project_is_active_alter_requestitem_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='slug',
            field=models.SlugField(auto_created=True, default=1),
            preserve_default=False,
        ),
    ]
