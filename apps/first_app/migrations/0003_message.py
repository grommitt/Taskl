# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-06-15 01:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0002_remove_task_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('created_on', models.DateField(auto_now_add=True)),
                ('updated_on', models.DateField(auto_now=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='author', to='first_app.Membership')),
                ('uploader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='first_app.Membership')),
            ],
        ),
    ]