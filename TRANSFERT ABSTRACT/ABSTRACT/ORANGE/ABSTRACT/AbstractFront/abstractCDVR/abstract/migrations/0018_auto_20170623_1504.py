# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-23 15:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('abstract', '0017_auto_20170623_1500'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chaine',
            options={'verbose_name': 'La Chaines', 'verbose_name_plural': 'Les Chaines du VSPP'},
        ),
        migrations.AlterModelOptions(
            name='listedemode',
            options={'verbose_name': 'Liste des Modes de Streaming', 'verbose_name_plural': 'Listes des Modes de Streaming'},
        ),
        migrations.AlterModelOptions(
            name='listedepod',
            options={'verbose_name': 'Liste des Pods', 'verbose_name_plural': 'Listes des Pods'},
        ),
        migrations.AlterModelOptions(
            name='mode',
            options={'verbose_name': 'Mode de Streaming', 'verbose_name_plural': 'Mode de Streaming'},
        ),
        migrations.AlterModelOptions(
            name='namechaine',
            options={'verbose_name': 'Nom des Chaines', 'verbose_name_plural': 'Noms des Chaines'},
        ),
        migrations.AlterModelOptions(
            name='namenode',
            options={'verbose_name': 'Les Noeud du VSPP ', 'verbose_name_plural': 'Les Noeud du VSPP '},
        ),
        migrations.AlterModelOptions(
            name='namepod',
            options={'verbose_name': 'Nom des Pods', 'verbose_name_plural': 'Noms des Pods'},
        ),
        migrations.AlterModelOptions(
            name='response',
            options={'verbose_name': 'Les r\xe9ponses des requ\xeates API VOD', 'verbose_name_plural': 'Les r\xe9ponses des requ\xeates API VOD'},
        ),
    ]