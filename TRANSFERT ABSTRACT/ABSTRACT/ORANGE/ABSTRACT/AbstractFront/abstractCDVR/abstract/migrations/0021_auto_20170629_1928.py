# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-29 19:28
from __future__ import unicode_literals

import abstract.extra
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_model_changes.changes


class Migration(migrations.Migration):

    dependencies = [
        ('abstract', '0020_auto_20170629_0927'),
    ]

    operations = [
        migrations.CreateModel(
            name='Documentation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Modop', help_text='Le document doit \xeatre en rapport \xe0 ABSTRACT', max_length=250, unique=True, verbose_name='Nom du document')),
                ('description', models.TextField()),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date de creation')),
                ('file', models.FileField(upload_to='documents/%Y/%m/%d', validators=[abstract.extra.validate_file_extension_docs])),
            ],
            options={
                'verbose_name': 'Document ',
                'verbose_name_plural': 'Documents ',
            },
        ),
        migrations.CreateModel(
            name='MyModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flag', models.BooleanField()),
            ],
            bases=(django_model_changes.changes.ChangesMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Sujet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=100)),
                ('content', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255)),
                ('entite', models.CharField(default='OLS', max_length=255)),
                ('ville', models.CharField(default='Rennes', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='YourModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_support_email', models.EmailField(blank=True, max_length=255, null=True)),
                ('marketing_email', models.EmailField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='configuration',
            name='schemadash',
            field=models.FileField(help_text="Choisir un fichier 'xsd' pour la validation des Manifests DASH", upload_to='schemas/dash/%Y/%m/%d', validators=[abstract.extra.validate_file_extension], verbose_name='Sch\xe9ma de validation des Manifests DASH'),
        ),
        migrations.AlterField(
            model_name='configuration',
            name='schemasmooth',
            field=models.FileField(help_text="Choisir un fichier 'xsd' pour la validation des Manifests SMOOTH", upload_to='schemas/smooth/%Y/%m/%d', validators=[abstract.extra.validate_file_extension], verbose_name='Sch\xe9ma de validation des Manifests SMOOTH'),
        ),
        migrations.AddField(
            model_name='sujet',
            name='auteur',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='abstract.User'),
        ),
    ]
