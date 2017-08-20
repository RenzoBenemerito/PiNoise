# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-20 05:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=45)),
                ('title', models.CharField(max_length=100)),
                ('category', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=5000)),
                ('date_posted', models.DateField(auto_now=True)),
                ('like', models.IntegerField()),
                ('dislike', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fName', models.CharField(max_length=45)),
                ('mName', models.CharField(max_length=45)),
                ('lName', models.CharField(max_length=45)),
                ('email', models.EmailField(max_length=100)),
                ('password', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='Votes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PiNoiseApp.Posts')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PiNoiseApp.Users')),
            ],
        ),
        migrations.AddField(
            model_name='posts',
            name='author_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PiNoiseApp.Users'),
        ),
        migrations.AddField(
            model_name='posts',
            name='category_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PiNoiseApp.Category'),
        ),
    ]
