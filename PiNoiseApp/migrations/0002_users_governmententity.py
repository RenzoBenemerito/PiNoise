# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-05 06:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PiNoiseApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='governmentEntity',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
