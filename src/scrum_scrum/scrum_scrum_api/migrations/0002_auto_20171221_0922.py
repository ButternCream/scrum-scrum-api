# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-21 09:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrum_scrum_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scrumscrumusertoken',
            name='key',
            field=models.CharField(max_length=40, primary_key=True, serialize=False, verbose_name='Key'),
        ),
    ]
