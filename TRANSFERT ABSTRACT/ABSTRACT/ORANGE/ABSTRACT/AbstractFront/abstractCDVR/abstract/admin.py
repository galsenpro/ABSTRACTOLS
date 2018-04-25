# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import *
from django.http import HttpResponse
from django.core import serializers

# Register your models here.
class StreamerAdmin(admin.ModelAdmin):
    #list_display = ('titre', 'headline', 'pub_date', 'apercu_contenu')
    list_display = ('address', 'created')
    list_filter = ('address', 'created')
    date_hierarchy = 'created'
    ordering = ('created',)
    search_fields = ('address', 'created')

class ChannelAdmin(admin.ModelAdmin):
    #list_display = ('titre', 'headline', 'pub_date', 'apercu_contenu')
    list_display = ('nom', 'description', 'created','pods')
    list_filter = ('nom', 'description', 'created','pods')
    date_hierarchy = 'created'
    ordering = ('created',)
    search_fields = ('nom', 'pods')

    # Configuration du formulaire d'édition
    fieldsets = (
        # Fieldset 1 : meta-info (titre, auteur…)
       ('Général', {
            'classes': ['collapse', ],
            'fields': ('nom',  'created','pods')
        }),
        # Fieldset 2 : contenu de l'article
        ('Contenu de la Chaine', {
           'description': 'Le formulaire accepte les balises HTML. Utilisez-les à bon escient !',
           'fields': ('description',)
        }),
    )

class CommandeAdmin(admin.ModelAdmin):
    #list_display = ('titre', 'headline', 'pub_date', 'apercu_contenu')
    list_display = ('nameCommande', 'description', 'created')
    list_filter = ('nameCommande', 'description', 'created')
    date_hierarchy = 'created'
    ordering = ('created',)
    search_fields = ('nameCommande',)

    # Configuration du formulaire d'édition
    fieldsets = (
        # Fieldset 1 : meta-info (titre, auteur…)
       ('Général', {
            'classes': ['collapse', ],
            'fields': ('nameCommande',  'created')
        }),
        # Fieldset 2 : contenu de l'article
        ('Détails', {
           'description': 'Le formulaire accepte les balises HTML. Utilisez-les à bon escient !',
           'fields': ('description',)
        }),
    )


class TypeCommandeAdmin(admin.ModelAdmin):
    #list_display = ('titre', 'headline', 'pub_date', 'apercu_contenu')
    list_display = ('name', 'period', 'start', 'end', 'description', 'created')
    list_filter = ('name', 'period', 'created')
    date_hierarchy = 'created'
    ordering = ('created',)
    search_fields = ('name',)
    fieldsets = (
        # Fieldset 1 : meta-info (titre, auteur…)
       ('Infos principales de la Commande', {
            'classes': ['collapse', ],
            'fields': ('name', 'period', 'start', 'end',  'created')
        }),
        # Fieldset 2 : contenu de l'article
        ('Description du Pod', {
           'description': 'Le formulaire accepte les balises HTML. Utilisez-les à bon escient !',
           'fields': ('commande', 'description',)
        }),
    )

class RequestAdmin(admin.ModelAdmin):
    #list_display = ('titre', 'headline', 'pub_date', 'apercu_contenu')
    list_display = ('nom', 'link', 'date', 'datareq', 'header')
    list_filter = ('nom', 'link', 'date', 'header')
    date_hierarchy = 'date'
    ordering = ('nom',)
    search_fields = ('nom', 'link','date', )

    # Configuration du formulaire d'édition
    fieldsets = (
        # Fieldset 1 : meta-info (titre, auteur…)
       ('Général', {
            'classes': ['collapse', ],
            'fields': ('nom', 'link', 'date')
        }),
        # Fieldset 2 : contenu de l'article
        ('Description de la requête', {
           'description': 'Le formulaire accepte les balises HTML. Utilisez-les à bon escient !',
           'fields': ('datareq', 'header')
        }),
    )

def test_manuel(modeladmin, request, queryset):
    #response = requests.post(str(link), data=datareq, headers={'Content-Type': 'application/xml'})
    #etat = response.status_code
    queryset.update(typetest='manuel')
test_manuel.short_description = "Refaire le test manuel - API VOD"

class ResponseAdmin(admin.ModelAdmin):
    list_display = ('nom', 'daterequest', 'datareq', 'status', 'body', 'typetest')
    readonly_fields=('typetest', )
    list_filter = ('nom', 'daterequest', 'link', 'datareq', 'status', 'reason', 'typetest')
    date_hierarchy = 'daterequest'
    ordering = ('daterequest', 'nom')
    search_fields = ('nom', 'daterequest', 'link', 'status', 'reason', 'typetest')
    actions = [test_manuel]
    # Configuration du formulaire d'édition
    fieldsets = (
       ('Général', {
            'classes': ['collapse', ],
            'fields': ('nom', 'daterequest', 'link', 'status', 'reason', 'methode', 'typetest' )
        }),
        # Fieldset 2 : Description
        ('Détails de la réponse reçue de l\'api VOD', {
           'description': 'Le formulaire accepte les balises HTML. Utilisez-les à bon escient !',
           'fields': ( 'datareq',  'body', 'header', 'duree')
        }),
    )

""" Modes """
class ModeAdminInline(admin.TabularInline):
    model = Mode

class ListeModeAdmin(admin.ModelAdmin):
    inlines = (ModeAdminInline, )

""" Commandes """

""" Pods """
class ChaineAdminInline(admin.TabularInline):
    model = Chaine

class StreamerAdminInline(admin.TabularInline):
    model = Streamer


class ListePodAdmin(admin.ModelAdmin):
    inlines = (ChaineAdminInline, StreamerAdminInline)
    list_display = ('name', 'created' )
    list_filter = ('name',  'created')
    date_hierarchy = 'created'
    ordering = ('created',)
    search_fields = ('name',)


class NamePodAdmin(admin.ModelAdmin):
    #list_display = ('titre', 'headline', 'pub_date', 'apercu_contenu')
    list_display = ('name', 'link','description', 'created')
    list_filter = ('name', 'link', 'description', 'created')
    date_hierarchy = 'created'
    ordering = ('created',)
    search_fields = ('name', 'link')

    # Configuration du formulaire d'édition
    fieldsets = (
        # Fieldset 1 : meta-info (titre, auteur…)
       ('Général', {
            'classes': ['collapse', ],
            'fields': ('name', 'link', 'created')
        }),
        # Fieldset 2 : contenu de l'article
        ('Contenu du Pod', {
           'description': 'Le formulaire accepte les balises HTML. Utilisez-les à bon escient !',
           'fields': ('description',)
        }),
    )

class ConfigurationAdmin(admin.ModelAdmin):
    #list_display = ('titre', 'headline', 'pub_date', 'apercu_contenu')
    list_display = ('nameConfig', 'vspp','protocole', 'port')
    list_filter = ('nameConfig', 'vspp','protocole', 'port')
    date_hierarchy = 'created'
    ordering = ('created',)
    search_fields = ('nameConfig', 'vspp','protocole', 'port')
    #inlines = [ListeDePodInline, ]
    # Configuration du formulaire d'édition
    fieldsets = (
       ('Paramètres généraux', {
            'classes': ['collapse', ],
            'fields': ('nameConfig', 'vspp','protocole', 'port',)
        }),
       ('Alertes & Validation', {
           'classes': ['collapse', ],
           'fields': ('intervalle', 'schemasmooth', 'schemadash',)
       }),
       ('Génération', {
           'classes': ['collapse', ],
           'fields': ('nameOfLevelFile', 'nameOfIframeFile', 'logprefixname',)
       }),
        ('Modes - Pods - Commandes', {
            'classes': ['collapse', ],
           'description': 'Blablablabla....',
           'fields': ('pods', 'commandesATraiter', 'modesATraiter',)
        }),
        ('Édition', {
           'fields': ('created',)
        }),
    )

class SujetAdmin(admin.ModelAdmin):
    #list_display = ('titre', 'headline', 'pub_date', 'apercu_contenu')
    list_display = ('titre', 'content','auteur',)
    list_filter = ('titre', 'content','auteur',)
    search_fields = ('titre', 'content','auteur',)
    #inlines = [ListeDePodInline, ]
    # Configuration du formulaire d'édition
    fieldsets = (
       ('Paramètres généraux', {
            'classes': ['collapse', ],
            'fields': ('titre','auteur',)
        }),
        ('Contenu', {
            'classes': ['collapse', ],
           'description': 'Blablablabla....',
           'fields': ('content',)
        }),
    )

###################" TESTS TABS ################

"""
def get_tabs(self, request, obj=None):
    tabs = self.tabs
    if obj is not None:
        tab_overview = self.tab_overview + ('Social', {
            'fields': ('website', 'twitter', 'facebook')
        })
        tab_ressources = self.tab_ressources + (InterviewInline, )
        tabs = [
            ('Overview', tab_overview),
            ('Ressources', tab_ressources)
        ]
    self.tabs = tabs
    return super(BandAdmin, self).get_tabs(request, obj)
"""

class ConfigurationFileAdmin(admin.ModelAdmin):

    actions = ['export_as_json']
    def export_as_json(modeladmin, request, queryset):
        response = HttpResponse(content_type="application/json")
        serializers.serialize("json", queryset, stream=response)
        return response

    #list_display = ('titre', 'headline', 'pub_date', 'apercu_contenu')
    list_display = ('vspp','port', 'schemasmooth', 'schemadash', 'file')
    list_filter = ('name', 'vspp','protocole', 'port', 'created', 'schemasmooth', 'schemadash', 'file')
    date_hierarchy = 'created'
    ordering = ('created',)
    search_fields = ('name', 'vspp','protocole', 'port', 'created')
    fieldsets = (
       ('Paramètres généraux', {
            'classes': ['collapse', ],
            'fields': ('name', 'vspp','protocole', 'port',)
        }),
       ('Validation', {
           'classes': ['collapse', ],
           'fields': ('intervalle', 'schemasmooth', 'schemadash',)
       }),
       ('Fichier de configuration', {
           'classes': ['collapse', ],
           'fields': ('file',)
       }),
       ('Génération', {
           'classes': ['collapse', ],
           'fields': ('nameOfLevelFile', 'nameOfIframeFile', 'logprefixname',)
       }),
        ('Édition', {
           'fields': ('created',)
        }),
    )

""" registre """
admin.site.register(NameChaine)
admin.site.register(CodeStreamer)
admin.site.register(NameNode)
admin.site.register(NamePod, NamePodAdmin)
admin.site.register(ListeDeMode, ListeModeAdmin)
admin.site.register(ListeDePod, ListePodAdmin)
##### API VOD #####
admin.site.register(Request, RequestAdmin)
admin.site.register(Response, ResponseAdmin)
##### Configuration pour le monitoring ######
admin.site.register(VSPP)
admin.site.register(Configuration, ConfigurationAdmin)
admin.site.register(ConfigurationFile, ConfigurationFileAdmin)
######### TESTS MODELES
admin.site.register(TypeProfilManifest)
""" Tests modules Django"""
admin.site.register(Documentation)