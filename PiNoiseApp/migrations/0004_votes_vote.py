# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-20 09:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PiNoiseApp', '0003_posts_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='votes',
            name='vote',
            field=models.CharField(default=None, max_length=45),
            preserve_default=False,
        ),
    ]