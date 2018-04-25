# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.translation import gettext as _
from .extra import *
# sudo pip install django-multiselectfield
from multiselectfield import MultiSelectField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.contenttypes.fields import GenericRelation  # Django 1.7+
#from django.contrib.contenttypes.generic import GenericRelation
# Create your models here.
"""
def __unicode__(self):
    return u'{}'.format(self.id)
"""

""" 
    PARTIE ABSTRACT MODELES
"""
NOMSREQUESTS = (('fetchfile', 'FETCH FILE'),
              ('TranscodingFiles', 'Transcoding Files'),
              ('CreateABRAsset', 'Create ABR Asset'),
             )
class Request(models.Model):
    nom = MultiSelectField(choices=NOMSREQUESTS, min_choices=1, max_choices=1, default='fetchfile',
                                         verbose_name="Nom de requête",
                                         )
    link = models.URLField(verbose_name="Lien de test", help_text="Exemple : http://192.168.134.3:5929/v2/fetch_file")
    datareq = models.TextField(verbose_name="Le contenu XML de test", help_text="Copier-coller le 'data' de la requête à tester")
    """
    Faire json en content-type
    """
    header = models.CharField(max_length=255, default="{'Content-Type': 'application/xml'}")
    date = models.DateTimeField(auto_now=False,
                               verbose_name="Date de creation", default= timezone.now)

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = 'Requête API VOD'
        verbose_name_plural =  'GESTION DES REQUETES API VOD'

class Response(models.Model):
    nom = MultiSelectField(choices=NOMSREQUESTS, min_choices=1, max_choices=1, default='fetchfile',
                           verbose_name="Nom de requête",
                           help_text="Choisir un seul type", )
    daterequest = models.DateTimeField(auto_now=False, default= timezone.now, verbose_name="Date", help_text="La date est mise à jour après un test manuel")
    link = models.URLField(verbose_name="Lien de test", help_text="Lien du test")
    datareq = models.TextField(verbose_name="Data", help_text="Données d'entrée de test")
    status = models.CharField(max_length=10, verbose_name="Status du retour de test", help_text="200 | 400 | 401 |500 ...")
    reason = models.CharField(max_length=255, verbose_name="Raison du statut", help_text="Ex: Not Found ")
    methode = models.CharField(max_length=100, verbose_name="Type requête", help_text="Ex : POST | GET ")
    body = models.TextField(verbose_name="Contenu de la réponse", help_text="Body")
    header = models.CharField(max_length=255)
    duree = models.CharField(max_length=255)
    typetest = models.CharField(max_length=6, default='auto', verbose_name="Manuel|Auto", help_text="Automatique par défaut")
    #fichier = models.FileField(upload_to='uploads/', default='kkg.txt')

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = 'Retour de test de l\'API VOD'
        verbose_name_plural =  'GESTION DES RETOURS DE TESTS API VOD'

class ListeDeMode(models.Model):
    name = models.CharField(max_length=128, verbose_name="Nom du mode de streaming", help_text="Merci de mettre en évidence SMOOTH, DASH ou HLS si utilisé")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Mode de Streaming'
        verbose_name_plural =  'GESTION MODES STREAMING'

NAMESMODES = (('smooth', 'SMOOTH'),
              ('dash', 'dash'),
              ('hls', 'HLS'),
             )
STATICABR = (('shss', 'shss pour le SMOOTH'),
              ('sdash', 'dash pour le DASH'),
              ('shls', 'shls pour le HLS'),
             )
MANIFESTSUFFIX = (('ism', 'ism pour le SMOOTH'),
              ('mpd', 'mpd pour le DASH'),
              ('m3u8', 'm3u8 pour le HLS'),
             )
DEVICESPROFILS = (('SMOOTH_2S', 'SMOOTH_2S pour le SMOOTH'),
              ('DASH_2S', 'DASH_2S pour le DASH'),
              ('HLS_LOW', 'HLS_LOW pour le HLS'),
             )
class Mode(models.Model):
    objet = models.ForeignKey(ListeDeMode)
    nameMode = MultiSelectField(choices=NAMESMODES, min_choices=1, max_choices=1, default='smooth',
                           verbose_name="Nom du mode",)
    staticAbr = MultiSelectField(choices=STATICABR, min_choices=1, max_choices=1, default='shss',
                           verbose_name="Static ABR",
                           help_text="Le static abr doit correspondre au mode choisi", )
    fragment = models.IntegerField(
        default=2,
        validators=[MaxValueValidator(10), MinValueValidator(2)],
        verbose_name="Taille du fragment", help_text="2 pour SMOOTH | 2 ou 4 pour DASH | 10 pour HLS")
    manifestSuffix = MultiSelectField(choices=MANIFESTSUFFIX, min_choices=1, max_choices=1, default='ism',
                           verbose_name="Manifest Suffix",
                           help_text="Le Manifest suffix doit correspondre au mode choisi", )
    deviceProfil = MultiSelectField(choices=DEVICESPROFILS, min_choices=1, max_choices=1, default='SMOOTH_2S',
                           verbose_name="Device profil",
                           help_text="Le Device profil doit correspondre au mode choisi", )

    def __str__(self):
        return self.nameMode

    class Meta:
        verbose_name = 'Mode de Streaming'
        verbose_name_plural =  'GESTION DES MODES STREAMING'

class NamePod(models.Model):
    name = models.CharField(max_length=100, unique=True)
    link = models.CharField(max_length=100,default='strm.podX.manager.cdvr.orange.fr', unique=True)
    description = models.TextField(null=True, default='Description du Pod')
    created = models.DateTimeField(auto_now=False,
                               verbose_name="Date de creation", default= timezone.now)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Pod d\'un VSPP'
        verbose_name_plural =  'GESTION DES PODS'

class ListeDePod(models.Model):
    name = models.ForeignKey(NamePod, blank=True, null=True, verbose_name="Libellé de la liste", help_text="Libellé de la liste de pods ")
    created = models.DateTimeField(auto_now=False,
                               verbose_name="Date de creation", default= timezone.now)
    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Liste de Pods'
        verbose_name_plural =  'GESTION DE LA LISTE DES PODS'

class NameChaine(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom de la Chaine", help_text="Ex: ARTE, CH_1, CH_2, etc.")
    description = models.TextField(default='Description de la Chaine')
    created = models.DateTimeField(auto_now=False,
                               verbose_name="Date d'enregistrement", default= timezone.now)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Nom de Chaine'
        verbose_name_plural =  'GESTION DES CHAINES TV DU VSPP'

class Chaine(models.Model):
    objet = models.ForeignKey(ListeDePod)
    name = models.ForeignKey(NameChaine, verbose_name="Nom de la Chaine", help_text="")

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Chaine'
        verbose_name_plural =  'GESTION LES CHAINES TV'


class CodeStreamer(models.Model):
    name = models.CharField(max_length=100, verbose_name="Code du Streamer", help_text="Ex: NODEA1, NODEB1, etc..")
    description = models.TextField(default='Description du streamer')
    created = models.DateTimeField(auto_now=False,
                               verbose_name="Date d'enregistrement de ce streamer", default= timezone.now)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Code Streamer'
        verbose_name_plural =  'GESTION DES CODES STREAMERS'

class NameNode(models.Model):
    name = models.ForeignKey(CodeStreamer, verbose_name="Nom du streamer", help_text="Voir Code Streamer")
    created = models.DateTimeField(auto_now=False,
                               verbose_name="Date de creation", default= timezone.now)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Noeud du VSPP '
        verbose_name_plural =  'GESTION DES NODES DU VSPP'

class Streamer(models.Model):
    objet = models.ForeignKey(ListeDePod, blank=True, null=True)
    node = models.ForeignKey(NameNode, blank=True, null=True, verbose_name="Nom du noeud", help_text="Nom du Noeud")
    address = models.GenericIPAddressField(protocol="ipv4", unpack_ipv4=False, verbose_name="Adresse du Streamer", help_text="Ex: 192.168.134.65")
    created = models.DateTimeField(auto_now=False,
                               verbose_name="Date de creation", default= timezone.now)

    def __str__(self):
        return str(self.address)

COMMANDES = (('live', 'LIVE'),
              ('catchup', 'CATCHUP'),
              ('startover', 'STARTOVER'),
              ('vodplayout', 'VOD PLAYOUT'),
              ('vodprepackaged', 'VOD PREPACKAGED'),
              ('ntc', 'NTC'),
              ('npvr', 'nPVR')
             )
MODES = (
    ( "['smooth': { 'staticabr': 'shss', 'fragment': '2', 'manifestsuffix': 'ism', device': 'SMOOTH_2S',client: null }]", _('SMOOTH')),
    ( "['dash': { 'staticabr': 'sdash', 'fragment': '2', 'manifestsuffix': 'mpd', device': 'DASH_2S',client: null }]", _('DASH')),
    ( "['hls': { 'staticabr': 'shls', 'fragment': '10', 'manifestsuffix': 'm3u8', device': 'HLS_LOW',client: null }]", _('HLS')),
)

class VSPP(models.Model):
    name = models.CharField(max_length=250, default='MISTRAL', unique = True, verbose_name="Nom du VSSP", help_text="Ex: MISTRAL, le VSPP de test par défaut")
    description = models.TextField()
    date = models.DateTimeField(auto_now=False,
                               verbose_name="Date de creation", default= timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'VSPP '
        verbose_name_plural =  'GESTION DES VSPP (MISTRAL par défaut)'


class Configuration(models.Model):
    HTTP = 'http'
    HTTPS = 'https'
    #FTP = 'ftp'
    PROTOCOLE_CHOICES = (
        (HTTP, 'http'),
        (HTTPS, 'https'),
       # (FTP, 'ftp'),
    )
    nameConfig = models.CharField(max_length=100, verbose_name="Libellé de la config", help_text="Merci de donner un libelle explicite")
    vspp = models.ForeignKey(VSPP, on_delete=models.CASCADE, default=1)
    protocole = models.CharField(
        max_length=5,
        choices=PROTOCOLE_CHOICES,
        default=HTTP,
        verbose_name="Protocole utilisé par le VSPP", help_text="PS: MISTRAL utilise le protocole 'http'"
    )
    port = models.IntegerField(
        default=5555,
        validators=[MaxValueValidator(5555), MinValueValidator(5555)],
        verbose_name="N° de port", help_text="5555 pour VSPP MISTRAL"
     )
    intervalle = models.IntegerField(
        default=10,
        validators=[MaxValueValidator(100), MinValueValidator(5)],
        verbose_name="Tps d'intervalle de tests", help_text="10s par défaut"
     )
    emailFrom = models.EmailField(default='adama.dieng@orange.com', editable=False)
    smsFrom = models.CharField(max_length=13, default='+33768225617', editable=False)
    schemasmooth = models.FileField(upload_to="schemas/smooth/%Y/%m/%d", validators=[validate_file_extension],
                                    verbose_name="Schéma de validation des Manifests SMOOTH",
                                    help_text="Choisir un fichier 'xsd' pour la validation des Manifests SMOOTH")
    schemadash=  models.FileField(upload_to="schemas/dash/%Y/%m/%d", validators=[validate_file_extension],
                                    verbose_name="Schéma de validation des Manifests DASH",
                                    help_text="Choisir un fichier 'xsd' pour la validation des Manifests DASH")
    nameOfLevelFile= models.CharField(max_length=50, default='Level')
    #folderOfLevelFile= models.FilePathField(path="/home/adama/images", match="foo.*", recursive=True)
    folderOfLevelFile = models.CharField(max_length=150, editable=False,
                                         default='/home/adama/PROJET/ABSTRACT/AbstractBackend/Levels/')
    nameOfIframeFile= models.CharField(max_length=50, default='Iframe')
    folderOfIframeFile = models.CharField(max_length=150,editable=False,
                                          default='/home/adama/PROJET/ABSTRACT/AbstractBackend/Iframe/')
    livefoldersmooth = models.CharField(max_length=150,editable=False,
                                        default='/home/adama/PROJET/ABSTRACT/AbstractBackend/manifests/dynamic/MSS/Live/')
    catchupfoldersmooth = models.CharField(max_length=150,editable=False,
                                           default='/home/adama/PROJET/ABSTRACT/AbstractBackend/manifests/dynamic/MSS/Catchup/')
    livefolderdash = models.CharField(max_length=150,editable=False,
                                      default='/home/adama/PROJET/ABSTRACT/AbstractBackend/manifests/dynamic/DASH/Live/')
    catchupfolderdash =  models.CharField(max_length=150,editable=False,
                                      default='/home/adama/PROJET/ABSTRACT/AbstractBackend/manifests/dynamic/DASH/Catchup/')
    livefolderhls = models.CharField(max_length=150,editable=False,
                                     default='/home/adama/PROJET/ABSTRACT/AbstractBackend/manifests/dynamic/HLS/Live/')
    catchupfolderhls = models.CharField(max_length=150,editable=False,
                                        default='/home/adama/PROJET/ABSTRACT/AbstractBackend/manifests/dynamic/HLS/Catchup/')
    logdirectory = models.CharField(max_length=150,editable=False,
                                    default='/home/adama/PROJET/ABSTRACT/AbstractBackend/logabstract',
                                    verbose_name="Dossier des logs ABSTRACT",
                                    help_text="Ce dossier contient le fichier de logs ABSTRACT")
    logprefixname = models.CharField(max_length=50, default='abstractLog',
                                     verbose_name="Nom du fichier log ABSTRACT",
                                     help_text="Fichier log")
    created = models.DateTimeField(auto_now=False,
                               verbose_name="Date de creation",
                                   default= timezone.now)
    pods = models.ManyToManyField(ListeDePod)
    #modes = models.ManyToManyField(ListeDeMode)
    commandesATraiter = MultiSelectField(choices=COMMANDES, min_choices=1, default='live',
                                         verbose_name="Commandes",
                                         help_text="LIVE, CATCHUP, VOD, etc.",)
    modesATraiter = MultiSelectField(choices=MODES, min_choices=3, verbose_name="Modes", help_text="SMOOTH, DASH, HLS")
    def __str__(self):
        return str(self.nameConfig)


    class Meta:
        verbose_name = 'Configuration'
        verbose_name_plural =  'CONFIG (avancée - doing)'

class Document(models.Model):
    file = models.FileField(upload_to="documents/%Y/%m/%d", validators=[validate_file_extension])



TYPEPROFILS = (('dynamic', 'Depuis un modèle Manifest'),
              ('static', 'Enregistrer mon propre profil Manifest'),
             )

class TypeProfilManifest(models.Model):
    try:
        typeProfil = MultiSelectField(choices=TYPEPROFILS, min_choices=1, max_choices=1,
                                        verbose_name="Mode de profil",
                                         help_text="Choisir votre type de profil à charger pour les tests Manifests")
        createdProfil = models.DateTimeField(auto_now=False,
                                    verbose_name="Date de création du Profil Manifest",
                                             default=timezone.now)
    except Exception as x:
        print(x)

""" PROFIL MANIFESTS """
"""
class ProfilSmooth(models.Model):
    nomProfilSmooth = models.CharField(max_length=100)

    DurationMin = models.CharField(max_length=100)
    DurationMax = models.CharField(max_length=100)
    MajorVersionMin = models.CharField(max_length=100)
    MajorVersionMax = models.CharField(max_length=100)
    LookAheadFragmentCountMin = models.CharField(max_length=100)
    LookAheadFragmentCountMax = models.CharField(max_length=100)
    DVRWindowLengthMin = models.CharField(max_length=100)
    DVRWindowLengthMax = models.CharField(max_length=100)
    MinorVersion = models.CharField(max_length=100)
    CanPause = models.CharField(max_length=100)
    IsLive = models.CharField(max_length=100)
    CanSeek = models.CharField(max_length=100)

    nbreChunksStreamAudio = models.CharField(max_length=100)
    nbreQualityLevelsStreamAudio  = models.CharField(max_length=100)
    NameStreamAudio = models.CharField(max_length=100)
    LanguageStreamAudio = models.CharField(max_length=100)

    nbreChunksStreamVideo = models.CharField(max_length=100)
    nbreQualityLevelsStreamVideo = models.CharField(max_length=100)

    BitrateQualityLevelVideo = models.CharField(max_length=100)
    MaxHeightQualityLevelVideo = models.CharField(max_length=100)
    MaxWidthQualityLevelVideo = models.CharField(max_length=100)
    FourCC = models.CharField(max_length=100)
    CodecPrivateData = models.CharField(max_length=100)

    BitsPerSampleQualityLevelAudio = models.CharField(max_length=100)
    PacketSizeQualityLevelAudio = models.CharField(max_length=100)
    AudioTagQualityLevelAudio = models.CharField(max_length=100)
    ChannelsQualityLevelAudio = models.CharField(max_length=100)
    SamplingRateQualityLevelAudio = models.CharField(max_length=100)
    BitrateMinQualityLevelAudio = models.CharField(max_length=100)
    BitrateMaxQualityLevelAudio = models.CharField(max_length=100)
    FourCCQualityLevelAudio = models.CharField(max_length=100)
    CodecPrivateDataQualityLevelAudio = models.CharField(max_length=100)

    tChunksAudioMin = models.CharField(max_length=100)
    tChunksAudioMax = models.CharField(max_length=100)
    dChunksAudioMin = models.CharField(max_length=100)
    dChunksAudioMax = models.CharField(max_length=100)

    tChunksVideoMin = models.CharField(max_length=100)
    tChunksVideoMax = models.CharField(max_length=100)
    dChunksVideoMin = models.CharField(max_length=100)
    dChunksVideoMax = models.CharField(max_length=100)

    description = models.TextField(default='Description du profil Smooth')
    created = models.DateTimeField(auto_now=False,
                               verbose_name="Date de creation", default= timezone.now)
"""
"""
from django.contrib.postgres.fields import ArrayField

class Item(models.Model):
    title = models.CharField(max_length=128)
    keywords = ArrayField(
        models.CharField(max_length=32, blank=True),
        default=list,
        blank=True,
    )
"""

class Documentation(models.Model):
    name = models.CharField(max_length=250, default='Modop', unique = True, verbose_name="Nom du document", help_text="Le document doit être en rapport à ABSTRACT")
    description = models.TextField()
    date = models.DateTimeField(auto_now=False,
                               verbose_name="Date de creation", default= timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Document '
        verbose_name_plural = 'DOCUMENTATION '
    file = models.FileField(upload_to="documents/%Y/%m/%d", validators=[validate_file_extension_docs])

class ConfigurationFile(models.Model):
    name = models.CharField(max_length=250, default='Configuration MISTRAL', unique = True, verbose_name="Nom de la configuration", help_text="Le document doit être en rapport à ABSTRACT")
    HTTP = 'http'
    HTTPS = 'https'
    #FTP = 'ftp'
    PROTOCOLE_CHOICES = (
        (HTTP, 'http'),
        (HTTPS, 'https'),
       # (FTP, 'ftp'),
    )
    vspp = models.ForeignKey(VSPP, on_delete=models.CASCADE, default=1)
    protocole = models.CharField(
        max_length=5,
        choices=PROTOCOLE_CHOICES,
        default=HTTP,
        verbose_name="Protocole utilisé par le VSPP", help_text="PS: MISTRAL utilise le protocole 'http'"
    )
    port = models.IntegerField(
        default=5555,
        validators=[MaxValueValidator(5555), MinValueValidator(5555)],
        verbose_name="N° de port", help_text="5555 pour VSPP MISTRAL"
     )
    intervalle = models.IntegerField(
        default=10,
        validators=[MaxValueValidator(100), MinValueValidator(5)],
        verbose_name="Tps d'intervalle de tests", help_text="10s par défaut"
     )
    emailFrom = models.EmailField(default='adama.dieng@orange.com', editable=False)
    smsFrom = models.CharField(max_length=13, default='+33768225617', editable=False)
    schemasmooth = models.FileField(upload_to="schemas/smooth/%Y/%m/%d", validators=[validate_file_extension],
                                    verbose_name="Schéma de validation SMOOTH",
                                    help_text="Choisir un fichier 'xsd' pour la validation SMOOTH")
    schemadash=  models.FileField(upload_to="schemas/dash/%Y/%m/%d", validators=[validate_file_extension],
                                    verbose_name="Schéma de validation DASH",
                                    help_text="Choisir un fichier 'xsd' pour la validation des Manifests DASH")
    nameOfLevelFile= models.CharField(max_length=50, default='Level')
    #folderOfLevelFile= models.FilePathField(path="/home/adama/images", match="foo.*", recursive=True)
    folderOfLevelFile = models.CharField(max_length=150, editable=False,
                                         default='/home/adama/PROJET/ABSTRACT/AbstractBackend/Levels/')
    nameOfIframeFile= models.CharField(max_length=50, default='Iframe')
    folderOfIframeFile = models.CharField(max_length=150,editable=False,
                                          default='/home/adama/PROJET/ABSTRACT/AbstractBackend/Iframe/')
    livefoldersmooth = models.CharField(max_length=150,editable=False,
                                        default='/home/adama/PROJET/ABSTRACT/AbstractBackend/manifests/dynamic/MSS/Live/')
    catchupfoldersmooth = models.CharField(max_length=150,editable=False,
                                           default='/home/adama/PROJET/ABSTRACT/AbstractBackend/manifests/dynamic/MSS/Catchup/')
    livefolderdash = models.CharField(max_length=150,editable=False,
                                      default='/home/adama/PROJET/ABSTRACT/AbstractBackend/manifests/dynamic/DASH/Live/')
    catchupfolderdash =  models.CharField(max_length=150,editable=False,
                                      default='/home/adama/PROJET/ABSTRACT/AbstractBackend/manifests/dynamic/DASH/Catchup/')
    livefolderhls = models.CharField(max_length=150,editable=False,
                                     default='/home/adama/PROJET/ABSTRACT/AbstractBackend/manifests/dynamic/HLS/Live/')
    catchupfolderhls = models.CharField(max_length=150,editable=False,
                                        default='/home/adama/PROJET/ABSTRACT/AbstractBackend/manifests/dynamic/HLS/Catchup/')
    logdirectory = models.CharField(max_length=150,editable=False,
                                    default='/home/adama/PROJET/ABSTRACT/AbstractBackend/logabstract',
                                    verbose_name="Dossier des logs ABSTRACT",
                                    help_text="Ce dossier contient le fichier de logs ABSTRACT")
    logprefixname = models.CharField(max_length=50, default='abstractLog',
                                     verbose_name="Nom du fichier log ABSTRACT",
                                     help_text="Fichier log")
    created = models.DateTimeField(auto_now=False,
                               verbose_name="Date de création de la configuration",
                                   default= timezone.now)

    file = models.FileField(upload_to="configs/%Y/%m/%d", validators=[validate_file_extensionjson],
                            verbose_name="Fichier config")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Configuration par Fichier (JSON)'
        verbose_name_plural = 'CONFIGURATION DES TESTS & MONITORING'

###### TEST DES TABS ##################"
