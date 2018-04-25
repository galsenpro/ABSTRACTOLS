# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-22 13:07
from __future__ import unicode_literals

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('abstract', '0002_auto_20170622_1250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='tags',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[(['skhks', 'lhlhl'], 'Sex'), ('work', 'Work'), ('happy', 'Happy'), ('food', 'Food'), ('field', 'Field'), ('boring', 'Boring'), ('interesting', 'Interesting'), ('huge', 'Huge'), ('nice', 'Nice')], max_length=71, null=True),
        ),
    ]
