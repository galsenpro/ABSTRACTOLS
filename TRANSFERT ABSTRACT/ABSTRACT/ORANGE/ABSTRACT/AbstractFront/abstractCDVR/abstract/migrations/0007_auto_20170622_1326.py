# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-22 13:26
from __future__ import unicode_literals

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('abstract', '0006_auto_20170622_1317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='tags',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[("['smooth': { 'staticabr': 'shss', 'fragment': '2', 'manifestsuffix': 'ism', device': 'SMOOTH_2S',client: null }]", 'SMOOTH'), ("['dash': { 'staticabr': 'sdash', 'fragment': '2', 'manifestsuffix': 'mpd', device': 'DASH_2S',client: null }]", 'DASH'), ("['hls': { 'staticabr': 'shls', 'fragment': '10', 'manifestsuffix': 'm3u8', device': 'HLS_LOW',client: null }]", 'HLS')], max_length=332, null=True),
        ),
    ]