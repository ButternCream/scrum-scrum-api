# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-20 05:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrum_scrum_api', '0003_auto_20171220_0527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scrumscrumuser',
            name='is_superuser',
            field=models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status'),
        ),
    ]