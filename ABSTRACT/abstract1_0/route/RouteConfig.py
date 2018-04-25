#!/usr/bin/python
#-*- coding: utf-8 -*-

import random
#import urllib2 - For Python 2.7

from lxml import etree                                                                                
import lxml  
import datetime
import time
from operator import or_
#from urllib.request import *
import urllib
import requests
from requests.exceptions import HTTPError
#from urllib2 import URLError - For Python 2.7
import cmd
import glob
import os
import json
import xmltodict
import errno
#import builtins
from influxdb import InfluxDBClient

from ipykernel import comm

from traitment.Traiter import *

class RouteConfig:
    def __init__(self):
        self.config = json.loads(open('/home/kirikou/ABSTRACT/abstract1_0/configs/configurations.json').read())
        
        #self.tree = etree.parse("configs/configurations.xml")
        self.listpods = []

        self.liststrms = []
        self.dictStrms = {"namepod": self.liststrms}
        self.listChaine = []
        self.dictChannels = {"adrStrm": self.listChaine}

        self.listpaterns = ["pat1", "pat2"]
        self.typeFile = "/Manifest"
        self.dictEmail = {}
        self.listAdr = []
         
    def getProtocole(self):
        try:
            return self.config['configs']['protocole']
        except Exception as x:
            self.createLogFile(x)
            
    def getPort(self):
        try:
            return self.config['configs']['port']
        except Exception as x:
            self.createLogFile(x)
            
    def getFolder(self, commande, mode):
        try:
            attribut = str(commande)+'folder'+str(mode)
            return self.config['configs'][attribut]
        except Exception as x:
            self.createLogFile(x)
    
    def getLogFolder(self):
        try:
            return self.config['configs']['logdirectory']
        except Exception as x:
            self.createLogFile(x)
            
    def getLogPrefix(self):
        try:
            return self.config['configs']['logprefixname']
        except Exception as x:
            self.createLogFile(x)
            
    def getIntervalle(self):
        try:
            return self.config['configs']['intervalle']
        except Exception as x:
            self.createLogFile(x)
            
    def getEmailFrom(self):
        try:
            print(self.config['configs']['emailFrom'])
            return self.config['configs']['emailFrom']
        except Exception as x:
            self.createLogFile(x)
            
    def getSmsFrom(self):
        try:
            return self.config['configs']['smsFrom']
        except Exception as x:
            self.createLogFile(x)

    def getTimeoutTest(self):
        for timeO in self.tree.xpath("/configs/timeout"):
            return timeO.text
        
    """Retourne une liste de Pods avec ses différents attributs"""
    def getPods(self):
        try:
            return self.config['configs']['pods']['pod']
        except Exception as x:
            self.createLogFile(x)
            
    def getSmoothSchema(self):
        try:
            return self.config['configs']['schemasmooth']
        except Exception as x:
            self.createLogFile(x)
    
    def getDashSchema(self):
        try:
            return self.config['configs']['schemadash']
        except Exception as x:
            self.createLogFile(x)
    
    def getAttributeOfPod(self, attribute):
        self.listpods =[]
        try:
            list = self.config['configs']['pods']['pod']
            for pod in list:
                self.listpods.append(pod.get(str(attribute)))
            return self.listpods
        except Exception as x:
            self.createLogFile(x)
    
    """Retourne la valeur de chaque attribut d'un Pod donné en paramètre"""
    
    def getValAttributeByPod(self,namePod, attribute):
        try:
            for element in self.config['configs']['pods']['pod']:
                if element.get("name") == str(namePod):                 
                    return element.get(str(attribute))
        except Exception as x:
            self.createLogFile(x)
            
    """ Retourne la liste des attributs de Streamers ou Chaines qui sont dans un Pod"""
    
    def getValAttributeStrmAndChannel(self,listStrm, attribute):
        listElements = []
        try:
            for str in listStrm:
                listElements.append((str.get(str(attribute))))
            return listElements
        except Exception as x:
            self.createLogFile(x)

    """Retourne la liste des Streamers Suivant un Pod bien défini """
    
    def getListStreamers(self, listDicoStr, attribute):
        malisteStr = []
        try:
            for element in listDicoStr:
                malisteStr.append(element.get(str(attribute)))
            return malisteStr
        except Exception as x:
            self.createLogFile(x)

    """Retourne la liste des Chaines Suivant un Pod bien ciblé """
    
    def getListChannels(self, DicoCh, attribute):
        malisteCh = []
        try:
            for element in DicoCh.values():
                malisteCh.append(element.get(str(attribute)))
            return malisteCh
        except AttributeError:
            for element in DicoCh.values():
                for el in element:
                    malisteCh.append(el.get(str(attribute)))
            return malisteCh
        except Exception as x:
            self.createLogFile(x)
    """  Ajout d'un nouveau   """
    def setPatern(self):
        self.dictpaterns['pat1'] = self.dictpods
        self.dictpaterns['pat2'] = self.dictstrms
        return self.dictpaterns
    
    """ Retourne un attribut d'un Mode dans le fichier de configuration """
    
    def getValAttributeOfMode(self,lemode, attribute):
        try:
            return self.config['configs']['modes'][str(lemode)][str(attribute)]
        except Exception as x :
            self.createLogFile(x)
            
    """ Retourne un attribut d'une Commande dans le fichier de configuration """
       
    def getValAttributeOfCommands(self,lacommande, attribute):
        try:
            return self.config['configs']['commands'][str(lacommande)][str(attribute)]
        except Exception as x :
            self.createLogFile(x)
    
    """ Exécution du Partern 1 : Routage par les Pods """
         
    def makePaternOne(self,commande = "catchup", mode="smooth" , *listeChannelsDistinctsPods):
        try:
            print("\n--PARTERN 1 : PODS :  "+str(mode).upper()+" on "+str(commande).upper()+" ...\n")
            protocole   = self.getProtocole()
            port   = self.getPort()
            abr    = self.getValAttributeOfMode(str(mode), "staticabr")
            frag    = self.getValAttributeOfMode(str(mode), "fragment")
            suffix    = self.getValAttributeOfMode(str(mode), "manifestsuffix")
            dev    = self.getValAttributeOfMode(str(mode), "device")
            
            startM = "LIVE"
            endM = "END"
            if mode.upper() == "HLS":
                self.typeFile =""
            else:
                self.typeFile="/Manifest"
                    
            if commande.upper() == "CATCHUP":
                fmt = '%Y-%m-%dT%H:%M:%S%ZZ'
                duree = self.getValAttributeOfCommands(str(commande), "period")
                startM = datetime.datetime.utcnow() + datetime.timedelta(hours= int(duree))
                endM = datetime.datetime.utcnow()
                endM = endM.strftime(fmt)
                startM = startM.strftime(fmt)
            else:
                startM = "LIVE"
                endM = "END"
                        
            listManifest = []
            listPods = self.getAttributeOfPod("link")
            
            for pod in listPods:
                nompod = pod[5:9]
                chs = self.getValAttributeByPod(str(nompod), "channels")
                liste = []
                for ch in chs.values():
                    if str(type(ch)) == "<type 'list'>":
                        choix = random.choice(ch)
                        chaine = choix.get("nom")
                    else:
                        chaine = ch.get("nom")
                manifest = protocole+"://"+ pod +":"+port+"/"+abr+"/LIVE$"+chaine+"/"+frag+"."+suffix+self.typeFile+"?start="+startM+"&end="+endM+"&device="+dev
                print(manifest)
                listManifest.append(manifest)
            return listManifest
        except Exception as x:
            self.createLogFile(x)
    
    """ Exécution du Patern 2 : Routage par les Streamers """
    
    def makePaternTwo(self,commande = "catchup", mode="smooth" , *listeChannelsDistinctsPods):
        try:
            print("\n--PARTERN 2 : STREAMERS :  "+str(mode).upper()+" on "+str(commande).upper()+" ...\n")
            protocole   = self.getProtocole()
            port   = self.getPort()
            abr    = self.getValAttributeOfMode(str(mode), "staticabr")
            frag    = self.getValAttributeOfMode(str(mode), "fragment")
            suffix    = self.getValAttributeOfMode(str(mode), "manifestsuffix")
            dev    = self.getValAttributeOfMode(str(mode), "device")
            
            startM = "LIVE"
            endM = "END"
            if mode.upper() == "HLS":
                self.typeFile =""
            else:
                self.typeFile="/Manifest"
                    
            if commande.upper() == "CATCHUP":
                fmt = '%Y-%m-%dT%H:%M:%S%ZZ'
                duree = self.getValAttributeOfCommands(str(commande), "period")
                startM = datetime.datetime.utcnow() + datetime.timedelta(hours= int(duree))
                endM = datetime.datetime.utcnow()
                endM = endM.strftime(fmt)
                startM = startM.strftime(fmt)
            else:
                startM = "LIVE"
                endM = "END"
            listManifest = []
            
            listPods = self.getAttributeOfPod("name")            
            for pod in listPods:
                chs = self.getValAttributeByPod(str(pod), "channels")
                podXStrm = self.getValAttributeByPod(str(pod), "streamer")
                liste = []
                for ch in chs.values():
                    if str(type(ch)) == "<type 'list'>":
                        choix = random.choice(ch)
                        chaine = choix.get("nom")
                    else:
                        chaine = ch.get("nom")
                    listAdress = self.getListStreamers(podXStrm, "address")
                    for adr in listAdress:
                        manifest = protocole+"://"+ adr +":"+port+"/"+abr+"/LIVE$"+chaine+"/"+frag+"."+suffix+self.typeFile+"?start="+startM+"&end="+endM+"&device="+dev
                        print(manifest)
                        listManifest.append(manifest)
            return listManifest
        except Exception as x:
            print(x)
            
    """ Exécution par choix aléatoire """
    
    def threader(self,listPartern, listCommands, listModes):
        try:
            patern = random.choice(listPartern)
            commandchoisi = random.choice(listCommands)
            modechoisi = random.choice(listModes)
            if str(patern).upper() == "PATERN1":
                listLinks = self.makePaternOne(commandchoisi, modechoisi)
            else:
                if str(patern).upper() == "PATERN2":
                    listLinks = self.makePaternTwo(commandchoisi, modechoisi)
                else:
                    return []
            return listLinks
        except Exception as x:
            self.createLogFile(x)
        
            
    """ Convert du Manifest en un flux JSON """
    def convert(self, manifest , xml_attribs=True):
        try:
            with open(str(manifest), "rb") as f:    # notice the "rb" mode
                d = xmltodict.parse(f, xml_attribs=xml_attribs)
                #f= json.dumps(d, indent=4)
                fh= open(str(manifest), 'w')
                fh.writelines(str(json.dumps(d, indent=4)).replace("@", ""))
                fh.close()
        except Exception as x:
            print(x)

    """ 
        Téléchargement de la liste de Manifests générés 
        Prend en params une liste de Manifests à Télécharger
        Puis passe l'exécution à la classe DB pour le DashBoard
    """         
    def download(self,manif):
        try:
            if str(manif[0]).find("hls") != -1:
                ManifestType = "hls"
                profil = "hls"
            else:
                if str(manif[0]).find("dash") != -1:
                    ManifestType = "dash"
                    profil = "dash"
                else:
                    ManifestType = "smooth"
                    profil = "smooth"
            for m in manif:
                fmtName = '%Y%m%d%H%M%S%Z'
                timeM= datetime.datetime.utcnow()
                elementB = m.split('$')[1]
                chaine = str(elementB).split('/')[0]                
                if m[19:21] == "65":
                    NodeName = "NODEA1"
                else:
                    if m[19:21] == "66":
                        NodeName = "NODEB1"
                    else:
                        if m[19:21] == "67":
                            NodeName = "NODEA2"
                        else:
                            NodeName = "NODEB2"
                    
                if "start=LIVE" in str(m):
                    commande = "live"
                else:
                    commande = "catchup"
                
                if str(m).find("strm") != -1:
                    NodeName = str(m[12:16]).upper()
                folder = self.getFolder(commande, ManifestType)
                """ Création du dossier des Manifests même s'il n'existe pas """
                self.creatingFolder(folder)
                try:
                    #self.createLogFile(m)
                    urllib.urlretrieve (m, folder+"/" +chaine+'_'+commande.upper()+ ManifestType.upper()+"_"+NodeName.upper()+"_"+timeM.strftime(fmtName))
                    #time.sleep(10)
                    """
                    VALIDATION - TEST - DB
                    """
                    file = folder+"/" +chaine+'_'+commande.upper()+ ManifestType.upper()+"_"+NodeName.upper()+"_"+timeM.strftime(fmtName)
                    if self.validManifest(file, profil)== True and str(m).find("shls") != -1:
                        if str(m).find("shls") != -1:
                            print("Fichier HLS Valide ")
                            with open(str(file), 'r') as content_file:
                                content = content_file.read()
                            print("Lien : "+m+"\n\
                                Nom Manifest :"+chaine+'_'+commande.upper()+ ManifestType.upper()+"_"+NodeName.upper()+"_"+timeM.strftime(fmtName)+"\n\
                                Noeud d'origine : "+NodeName.upper()+"\n\
                                Chaine : "+chaine+"\n\
                                Commande : "+commande.upper()+"\n\
                                Mode : "+ManifestType.upper()+"\n\
                                Date : "+timeM.strftime("%Y-%m-%d %H:%M:%S%Z")+"\n\
                                Message d'erreur : "+content+"\n") 
                        else:
                            print("Fichier HLS Invalide  :)! ")
                            with open(str(file), 'r') as content_file:
                                content = content_file.read()
                            print("Lien : "+m+"\n\
                                Nom Manifest :"+chaine+'_'+commande.upper()+ ManifestType.upper()+"_"+NodeName.upper()+"_"+timeM.strftime(fmtName)+"\n\
                                Noeud d'origine : "+NodeName.upper()+"\n\
                                Chaine : "+chaine+"\n\
                                Commande : "+commande.upper()+"\n\
                                Mode : "+ManifestType.upper()+"\n\
                                Date : "+timeM.strftime("%Y-%m-%d %H:%M:%S%Z")+"\n\
                                Message d'erreur : "+content+"\n")      
                    else:
                        if str(m).find("sdash") != -1 :
                            if self.validManifest(file, profil)== True:
                                print("--- Fichier DASH Valide ")
                                self.convert(file)
                                
                            else:
                                print(" Fichier DASH Invalide ---")
                                with open(str(file), 'r') as content_file:
                                    content = content_file.read()
                                print("Lien : "+m+"\n\
                                    Nom Manifest :"+chaine+'_'+commande.upper()+ ManifestType.upper()+"_"+NodeName.upper()+"_"+timeM.strftime(fmtName)+"\n\
                                    Noeud d'origine : "+NodeName.upper()+"\n\
                                    Chaine : "+chaine+"\n\
                                    Commande : "+commande.upper()+"\n\
                                    Mode : "+ManifestType.upper()+"\n\
                                    Date : "+timeM.strftime("%Y-%m-%d %H:%M:%S%Z")+"\n\
                                    Message d'erreur : "+content+"\n")
                        else:
                            if str(m).find("shss") != -1 :
                                if self.validManifest(file, profil)== True:
                                    print("--- Fichier SMOOTH Valide ")
                                    self.convert(file)
                                    test = Traiter(str(file))
                                    print('--------Flux JSON.....')
                                    jsonfile = test.generateBody(timeM.strftime("%Y-%m-%dT%H:%M:%S%Z"),commande.upper(),ManifestType.upper(),NodeName.upper())
                                    #print(file)
                                    client = InfluxDBClient('192.168.134.122', 8086, 'admin', 'admin', 'abstract1')
                                    #client.create_database('example')
                                    client.write_points(jsonfile)
                                else:
                                    print(" Fichier SMOOTH Invalide ---")
                                    with open(str(file), 'r') as content_file:
                                        content = content_file.read()
                                    print("Lien : "+m+"\n\
                                        Nom Manifest :"+chaine+'_'+commande.upper()+ ManifestType.upper()+"_"+NodeName.upper()+"_"+timeM.strftime(fmtName)+"\n\
                                        Noeud d'origine : "+NodeName.upper()+"\n\
                                        Chaine : "+chaine+"\n\
                                        Commande : "+commande.upper()+"\n\
                                        Mode : "+ManifestType.upper()+"\n\
                                        Date : "+timeM.strftime("%Y-%m-%d %H:%M:%S%Z")+"\n\
                                        Message d'erreur : "+content+"\n")   
                            else:
                                if str(m).find("shls") != -1 :
                                    with open(str(file), 'r') as content_file:
                                        content = content_file.read()
                                    print("Lien : "+m+"\n\
                                        Nom Manifest :"+chaine+'_'+commande.upper()+ ManifestType.upper()+"_"+NodeName.upper()+"_"+timeM.strftime(fmtName)+"\n\
                                        Noeud d'origine : "+NodeName.upper()+"\n\
                                        Chaine : "+chaine+"\n\
                                        Commande : "+commande.upper()+"\n\
                                        Mode : "+ManifestType.upper()+"\n\
                                        Date : "+timeM.strftime("%Y-%m-%d %H:%M:%S%Z")+"\n\
                                        Message d'erreur : "+content+"\n")
                except Exception as testDowload:
                    self.createLogFile(testDowload)
                #print(folder+"/" +commande.upper()+ ManifestType.upper()+"_"+NodeName.upper()+"_"+timeM.strftime(fmtName))
                #Changing with Python 3
                #time.sleep(2)
            return manif
        except Exception as x:
            self.createLogFile(x)
            return manif
    
    """ Néttoyage du dossier Manifests """
        
    def clean(self,folder):
        try:
            filelist = glob.glob(str(folder)+"*")
            for f in filelist:
                os.remove(f)
        except Exception as x:
            self.createLogFile(x)
    
    """ Création de l'emplacement des Manifests dans le fichier de configuration """
    
    def creatingFolder(self, folder):
        try:
            if not os.path.exists(folder):
                try:
                    os.makedirs(folder)
                except OSError as exc: # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise        
        except IOError:
            print("Impossible de créer le dossier "+ str(folder))
        except Exception as x:
            print(x)
            #self.createLogFile(x)
                        
    """ Crée un fichier log qui contient toutes les traces de Manifests à doowloader"""   
    def createLogFile(self, contentLog):
        try:
            fmt = '%Y%m%dT%H%M%S%ZZ'
            dateLog = datetime.datetime.utcnow()
            dateLog = dateLog.strftime(fmt)
            filename = self.getLogFolder()+"/"+self.getLogPrefix()+".log"
            if not os.path.exists(os.path.dirname(filename)):
                try:
                    os.makedirs(os.path.dirname(filename))
                except OSError as exc: # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise
            with open(filename, "a") as f:
                f.writelines(str(datetime.datetime.utcnow()) + ";"+str(contentLog)+"\n")
        
        except IOError:
            print("Fichier Manifest introuvable ! ")
        except Exception as x:
            print(x)
    
    """ Obtention des derniers Manifests recupérés """
    
    def getLastXMLFile(self, folder):
        try:
            files_path = os.path.join(folder, '*')
            files = sorted(
                glob.iglob(files_path), key=os.path.getctime, reverse=True)
            return files[:4]
        except Exception as x:
            self.createLogFile(x)
            
    
    """ Obtention des derniers Manifests recupérés en LIVE """
    
    def getLastXMLFileLIVE(self, folder):
        try:
            files_path = os.path.join(folder, '*')
            files = sorted(
                glob.iglob(files_path), key=os.path.getctime, reverse=True)
            #print (files[:10])
            return files[:4]
        except Exception as x :
            self.createLogFile(x)
            
    """ Obtention des derniers Manifests recupérés en CATCHUP """
    
    def getLastXMLFileCATCHUP(self, folder):
        try:
            files_path = os.path.join(folder, '*')
            files = sorted(
                glob.iglob(files_path), key=os.path.getctime, reverse=True)
            #print (files[:10])
            return files[:4]
        except Exception as x:
            self.createLogFile(x)
    
    def validManifest(self,file, profil = "smooth"):
        try:
            if profil == "smooth":
                schema = self.getSmoothSchema()
            else:
                if profil == "dash":
                    schema = self.getDashSchema()
                else:
                    profil = "hls"
            if profil == "smooth" or profil == "dash":
                with open(schema) as f:
                    valid = False                                             
                    tree = etree.parse(f)                                    
                try:                                                                        
                    schema = etree.XMLSchema(tree)
                    valid = True  
                    #print ("Le Schema est valide")                                          
                except lxml.etree.XMLSchemaParseError as e:
                    valid = False
                    print ("Schema incorrect!")
                """Validation Manifest """
                if valid == True:
                    with open(file) as f:
                        validManifest = False                                                
                        tree = etree.parse(f)                                                    
                    try:                                                                        
                        schema.assertValid(tree)
                        validManifest = True
                        #print ("Le Manifest est bien valide")                                             
                    except lxml.etree.DocumentInvalid as e:    
                        validManifest = False  
                        #print (e)                                                                   
                    return validManifest
                else:
                    return False
        except Exception as x:
            print ("Manifest invalide !")
            
    """Attribute of SmoothStreamingMedia"""
    
    def getAttribSmoothStreamingMedia(self, manifest, attribute =None):
        try:
            tree = etree.parse(manifest)
            if attribute ==None:
                dico = {}
                for smooth in tree.xpath("/SmoothStreamingMedia"):
                    dico = smooth.attrib
                #print (dico)
                return smooth.attrib
            else:
                for smooth in tree.xpath("/SmoothStreamingMedia"):
                    if smooth.get(attribute)==None:
                        #print ("Indispo")
                        return "Indispo"
                    else:
                        #print (attribute + " -> " + smooth.get(attribute))
                        return smooth.get(attribute)
                print ("\n")
                return smooth.get(attribute)
        except Exception as x:
            print (x)
            return x
    
    
    def getStreamIndexAttribute(self,manifest,typeStrIndex, attrStrm):
        liste = []
        try:
            tree = etree.parse(manifest)
            for strm in tree.xpath('/SmoothStreamingMedia/StreamIndex[Type="'+typeStrIndex+'"]'):
                return strm.get(attrStrm)
            else:
                #print ("Erreur")
                return "Erreur "
        except Exception as x:
            print (x)
         
    
    def getValueOfAttributeSmooth(self, dico , attribut = None):
        try:
            if attribut == None:
                for cle,valeur in dico.items():
                    print (cle, valeur)
            else:
                if dico.has_key(str(attribut)):
                    #print (dico.get(str(attribut)))
                    return dico.get(str(attribut)) 
        except Exception as x:
            print (x)   
    
    def getAttribStreamIndex(self, manifest, typeStrIndex):
        try:
            liste = []
            tree = etree.parse(manifest)
            for attrStrm in tree.xpath('/SmoothStreamingMedia/StreamIndex[Type="'+typeStrIndex+'"]'):
                liste.append(attrStrm.attrib)
            #print liste
            return liste
        except Exception as x:
            print (x)
    
    def getChunksAttribute(self, manifest, typeStrIndex, attrChunks):
        try:
            #print (typeStrIndex +" - "+ attrChunks)
            Valeurs = []
            tree = etree.parse(manifest)
            for chunk in tree.xpath('/SmoothStreamingMedia/StreamIndex[Type="'+typeStrIndex+'"]/c'):
                if chunk.get(attrChunks) != None:
                    Valeurs.append(chunk.get(attrChunks))
            #print Valeurs
            #print ":".join(Valeurs)
            #return ":".join(Valeurs)
            #print Valeurs
            return Valeurs
        except Exception as x:
            print (x)
              
    def getQualityLevelAttribute(self, manifest,typeStrIndex, attrQly=None):
        try:
            #print (typeStrIndex)
            tree = etree.parse(manifest)
            Valeurs = []
            for qly in tree.xpath('/SmoothStreamingMedia/StreamIndex[Type="'+typeStrIndex+'"]/QualityLevel'):
               # Valeurs.append(qly.get(attrQly))
                Valeurs.append(qly.attrib)
                #print(qly.attrib)
            #print attrQly + ";" .join(Valeurs)
            #return ":".join(Valeurs)
            return Valeurs
            #print Valeurs
        except Exception as x:
            print (x)
            return x
          
    """Getting the all type of StreamIndex"""
           
    def getTypeStreamIndex(self, manifest):
        try:
            listType =  []
            tree = etree.parse(manifest)
            for strm in tree.xpath("/SmoothStreamingMedia/StreamIndex"):
                listType.append(strm.get('Type'))
            #print (listType)
            return listType
        except Exception as x:
            print (x)
    def TypeStreamIndexIsPresent(self, liste):
        try:
            if len(liste)!=2:
                print ("Manifest incorrect !")
        except Exception as x:
            print (x)
test = RouteConfig()
#test.createLogFile("Contenu de mon log")
"""
test.creatingFolder("/home/kirikou/manifests/dynamic/MSS/Live/")
test.creatingFolder("/home/kirikou/manifests/dynamic/MSS/Catchup/")
test.creatingFolder("/home/kirikou/manifests/dynamic/DASH/Live/")
test.creatingFolder("/home/kirikou/manifests/dynamic/DASH/Catchup/")
test.creatingFolder("/home/kirikou/manifests/dynamic/HLS/Live/")
test.creatingFolder("/home/kirikou/manifests/dynamic/HLS/Catchup/")
"""
while 1:
    links = test.threader(["PATERN1","PATERN2"], ["live", "catchup"], ["smooth","dash", "hls"])
    test.download(links)
    #test.clean(folder)
 