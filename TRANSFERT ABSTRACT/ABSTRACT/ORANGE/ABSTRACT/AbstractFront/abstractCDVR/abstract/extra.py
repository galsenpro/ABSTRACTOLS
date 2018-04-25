#-*- coding: utf-8 -*-#
import os
from django.core.exceptions import ValidationError

def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.xsd']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Le fichier doit etre un xsd !')

def validate_file_extensionjson(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.json']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Fichier de configuration non valide !')

def validate_file_xsd(value):
    try:
        ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
        valid_extensions = ['.xsd']
        if not ext.lower() in valid_extensions:
            raise ValidationError(u'Unsupported file extension.')
    except Exception as x:
        print(x)
def validate_file_extension_docs(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.xml', '.csv', '.doc', '.pdf', '.jpg', '.png', 'gif', '.jpeg', '.ppt']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Unsupported file extension.')

def generateConfig():
    try:
        print("Génération d'une configuration ...")
        #print(DEBUG)
        from django.core import serializers
        from abstract import models
        data = serializers.serialize("json", models.MyModel.objects.all())
        out = open("mymodel.json", "w")
        out.write(data)
        out.close()
    except Exception as x:
        print(x)

#generateConfig()

