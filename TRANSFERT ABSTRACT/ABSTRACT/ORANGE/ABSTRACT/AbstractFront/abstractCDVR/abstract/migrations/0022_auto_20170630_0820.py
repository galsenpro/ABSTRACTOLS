# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-30 08:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('abstract', '0021_auto_20170629_1928'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sujet',
            name='auteur',
        ),
        migrations.DeleteModel(
            name='Sujet',
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
