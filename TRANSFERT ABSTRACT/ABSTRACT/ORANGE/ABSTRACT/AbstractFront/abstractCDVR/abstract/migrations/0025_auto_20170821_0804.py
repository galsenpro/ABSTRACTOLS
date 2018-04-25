# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-21 08:04
from __future__ import unicode_literals

import abstract.extra
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('abstract', '0024_auto_20170630_1216'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfigFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Configuration MISTRAL', help_text='Le document doit \xeatre en rapport \xe0 ABSTRACT', max_length=250, unique=True, verbose_name='Nom de la configuration')),
                ('description', models.TextField()),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date de cr\xe9ation de la configuration')),
                ('file', models.FileField(upload_to='configs/%Y/%m/%d', validators=[abstract.extra.validate_file_extensionjson])),
            ],
            options={
                'verbose_name': 'Configuration par Fichier (JSON)',
                'verbose_name_plural': 'Configurations par Fichier (JSON) ',
            },
        ),
        migrations.DeleteModel(
            name='Book',
        ),
        migrations.AlterModelOptions(
            name='configuration',
            options={'verbose_name': 'Configuration (avanc\xe9e)', 'verbose_name_plural': 'Configurations (avanc\xe9e)'},
        ),
    ]