# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-22 19:58
from __future__ import unicode_literals

import abstract.extra
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abstract', '0014_auto_20170622_1408'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configuration',
            name='schemadash',
            field=models.FileField(upload_to='schemas/dash/%Y/%m/%d', validators=[abstract.extra.validate_file_xsd]),
        ),
        migrations.AlterField(
            model_name='configuration',
            name='schemasmooth',
            field=models.FileField(upload_to='schemas/smooth/%Y/%m/%d', validators=[abstract.extra.validate_file_xsd]),
        ),
    ]
