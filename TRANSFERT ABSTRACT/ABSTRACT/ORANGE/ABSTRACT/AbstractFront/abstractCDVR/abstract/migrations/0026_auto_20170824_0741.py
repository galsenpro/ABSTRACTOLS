# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-24 07:41
from __future__ import unicode_literals

import abstract.extra
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('abstract', '0025_auto_20170821_0804'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfigurationFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Configuration MISTRAL', help_text='Le document doit \xeatre en rapport \xe0 ABSTRACT', max_length=250, unique=True, verbose_name='Nom de la configuration')),
                ('protocole', models.CharField(choices=[('http', 'http'), ('https', 'https')], default='http', help_text="PS: MISTRAL utilise le protocole 'http'", max_length=5, verbose_name='Protocole utilis\xe9 par le VSPP')),
                ('port', models.IntegerField(default=5555, help_text='5555 pour VSPP MISTRAL', validators=[django.core.validators.MaxValueValidator(5555), django.core.validators.MinValueValidator(5555)], verbose_name='N\xb0 de port')),
                ('intervalle', models.IntegerField(default=10, help_text='10s par d\xe9faut', validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(5)], verbose_name="Tps d'intervalle de tests")),
                ('emailFrom', models.EmailField(default='adama.dieng@orange.com', editable=False, max_length=254)),
                ('smsFrom', models.CharField(default='+33768225617', editable=False, max_length=13)),
                ('schemasmooth', models.FileField(help_text="Choisir un fichier 'xsd' pour la validation SMOOTH", upload_to='schemas/smooth/%Y/%m/%d', validators=[abstract.extra.validate_file_extension], verbose_name='Sch\xe9ma de validation SMOOTH')),
                ('schemadash', models.FileField(help_text="Choisir un fichier 'xsd' pour la validation des Manifests DASH", upload_to='schemas/dash/%Y/%m/%d', validators=[abstract.extra.validate_file_extension], verbose_name='Sch\xe9ma de validation DASH')),
                ('nameOfLevelFile', models.CharField(default='Level', max_length=50)),
                ('folderOfLevelFile', models.CharField(default='/home/adama/PROJET/ABSTRACT/AbstractBackend/Levels/', editable=False, max_length=150)),
                ('nameOfIframeFile', models.CharField(default='Iframe', max_length=50)),
                ('folderOfIframeFile', models.CharField(default='/home/adama/PROJET/ABSTRACT/AbstractBackend/Iframe/', editable=False, max_length=150)),
                ('livefoldersmooth', models.CharField(default='/home/adama/PROJET/ABSTRACT/AbstractBackend/manifests/dynamic/MSS/Live/', editable=False, max_length=150)),
                ('catchupfoldersmooth', models.CharField(default='/home/adama/PROJET/ABSTRACT/AbstractBackend/manifests/dynamic/MSS/Catchup/', editable=False, max_length=150)),
                ('livefolderdash', models.CharField(default='/home/adama/PROJET/ABSTRACT/AbstractBackend/manifests/dynamic/DASH/Live/', editable=False, max_length=150)),
                ('catchupfolderdash', models.CharField(default='/home/adama/PROJET/ABSTRACT/AbstractBackend/manifests/dynamic/DASH/Catchup/', editable=False, max_length=150)),
                ('livefolderhls', models.CharField(default='/home/adama/PROJET/ABSTRACT/AbstractBackend/manifests/dynamic/HLS/Live/', editable=False, max_length=150)),
                ('catchupfolderhls', models.CharField(default='/home/adama/PROJET/ABSTRACT/AbstractBackend/manifests/dynamic/HLS/Catchup/', editable=False, max_length=150)),
                ('logdirectory', models.CharField(default='/home/adama/PROJET/ABSTRACT/AbstractBackend/logabstract', editable=False, help_text='Ce dossier contient le fichier de logs ABSTRACT', max_length=150, verbose_name='Dossier des logs ABSTRACT')),
                ('logprefixname', models.CharField(default='abstractLog', help_text='Fichier log', max_length=50, verbose_name='Nom du fichier log ABSTRACT')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date de cr\xe9ation de la configuration')),
                ('file', models.FileField(upload_to='configs/%Y/%m/%d', validators=[abstract.extra.validate_file_extensionjson], verbose_name='Fichier config')),
            ],
            options={
                'verbose_name': 'Configuration par Fichier (JSON)',
                'verbose_name_plural': 'CONFIGURATION DES TESTS & MONITORING',
            },
        ),
        migrations.DeleteModel(
            name='ConfigFile',
        ),
        migrations.AlterModelOptions(
            name='chaine',
            options={'verbose_name': 'Chaine', 'verbose_name_plural': 'GESTION LES CHAINES TV'},
        ),
        migrations.AlterModelOptions(
            name='codestreamer',
            options={'verbose_name': 'Code Streamer', 'verbose_name_plural': 'GESTION DES CODES STREAMERS'},
        ),
        migrations.AlterModelOptions(
            name='configuration',
            options={'verbose_name': 'Configuration', 'verbose_name_plural': 'CONFIG (avanc\xe9e - doing)'},
        ),
        migrations.AlterModelOptions(
            name='documentation',
            options={'verbose_name': 'Document ', 'verbose_name_plural': 'DOCUMENTATION '},
        ),
        migrations.AlterModelOptions(
            name='listedemode',
            options={'verbose_name': 'Mode de Streaming', 'verbose_name_plural': 'GESTION MODES STREAMING'},
        ),
        migrations.AlterModelOptions(
            name='listedepod',
            options={'verbose_name': 'Liste de Pods', 'verbose_name_plural': 'GESTION DE LA LISTE DES PODS'},
        ),
        migrations.AlterModelOptions(
            name='mode',
            options={'verbose_name': 'Mode de Streaming', 'verbose_name_plural': 'GESTION DES MODES STREAMING'},
        ),
        migrations.AlterModelOptions(
            name='namechaine',
            options={'verbose_name': 'Nom de Chaine', 'verbose_name_plural': 'GESTION DES CHAINES TV DU VSPP'},
        ),
        migrations.AlterModelOptions(
            name='namenode',
            options={'verbose_name': 'Noeud du VSPP ', 'verbose_name_plural': 'GESTION DES NODES DU VSPP'},
        ),
        migrations.AlterModelOptions(
            name='namepod',
            options={'verbose_name': "Pod d'un VSPP", 'verbose_name_plural': 'GESTION DES PODS'},
        ),
        migrations.AlterModelOptions(
            name='request',
            options={'verbose_name': 'Requ\xeate API VOD', 'verbose_name_plural': 'GESTION DES REQUETES API VOD'},
        ),
        migrations.AlterModelOptions(
            name='response',
            options={'verbose_name': "Retour de test de l'API VOD", 'verbose_name_plural': 'GESTION DES RETOURS DE TESTS API VOD'},
        ),
        migrations.AlterModelOptions(
            name='vspp',
            options={'verbose_name': 'VSPP ', 'verbose_name_plural': 'GESTION DES VSPP (MISTRAL par d\xe9faut)'},
        ),
        migrations.AddField(
            model_name='configurationfile',
            name='vspp',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='abstract.VSPP'),
        ),
    ]
