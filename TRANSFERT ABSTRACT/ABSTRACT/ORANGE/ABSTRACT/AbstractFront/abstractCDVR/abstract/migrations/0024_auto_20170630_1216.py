# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-30 12:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('abstract', '0023_auto_20170630_0939'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='album',
            name='band',
        ),
        migrations.RemoveField(
            model_name='concert',
            name='band',
        ),
        migrations.RemoveField(
            model_name='interview',
            name='band',
        ),
        migrations.RemoveField(
            model_name='musician',
            name='band',
        ),
        migrations.DeleteModel(
            name='Album',
        ),
        migrations.DeleteModel(
            name='Band',
        ),
        migrations.DeleteModel(
            name='Concert',
        ),
        migrations.DeleteModel(
            name='Interview',
        ),
        migrations.DeleteModel(
            name='Musician',
        ),
    ]
