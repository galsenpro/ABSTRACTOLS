#!/usr/bin/python
#-*- coding: utf-8 -*-

from route.Route import *
#from database.BDD import *
from database.AccessDB import *
from validation.Validation import *
from recup.dataManifest import *
from influxdb import InfluxDBClient

import re
import datetime
json_body = []
measurement={}
tags ={}
tagsSmooth ={}
tagsStreamIndex={}
tagsStreamIndexAudio= {}

fields={}
fieldsSmooth = {}
filedsStreamIndex={}
filedsStreamIndexAudio={}
regex = re.compile(r"[0-9]*[a-zA-Z]+[0-9]*")

if __name__ == "__main__":
    i = 0
    """Boucle d'arrêt de mon script"""
    while 1 < 2: 
            """
            Création d'une Route pour faire du SMOOTH
            """
            routeMSS = Route()
            """
            On définit le type de fichier Manifest à recupèrer
            """
            mss = routeMSS.getManifest("CATCHUP", "smooth")
            #routeMSS.download(mss)
            """
            Idem pour DASH !
            """
            routeDASH = Route()
            dash = routeDASH.getManifest("CATCHUP", "dash")
            #routeDASH.download(dash)
            """
            Idem pour HLS !
            """
            routeHLS = Route()
            hls = routeHLS.getManifest("CATCHUP", "hls")
            #routeHLS.download(hls)
            print ("\n")
            """
            On choisit les 4 derniers fichiers à traiter dans une LISTE
            """
            listeMSS  = routeMSS.getLastXMLFile("/home/adama/NetBeansProjects/ABSTRACT1_0/abstract1_0/manifests/dynamic/MSS")
            listeDASH = routeDASH.getLastXMLFile("/home/adama/NetBeansProjects/ABSTRACT1_0/abstract1_0/manifests/dynamic/DASH")
            listeHLS  = routeHLS.getLastXMLFile("/home/adama/NetBeansProjects/ABSTRACT1_0/abstract1_0/manifests/dynamic/HLS")
            """
            TRAITEMENT DE CHAQUE FICHIER DE MES DIFFÉRENTES LISTES
            """
            for element in listeMSS:
                manifest = DataManifestMSS(element)
                """
                Validation du fichier Manifest avec le schéma donné
                """
                if manifest.validManifest()== True:
                    json_bodyCATCHUP = []
                    dic={}
                    
                    """ Nom du fichier dans le système """
                    NameSmooth = element.split("/")
                    NameSmooth= NameSmooth[len(NameSmooth)-1]
                    listdetails = NameSmooth.split("_")
                    dateSup = listdetails[len(listdetails)-1]
                    noeud = listdetails[len(listdetails)-2]
                    profil = listdetails[len(listdetails)-3]
                    commande = listdetails[len(listdetails)-4]
                    conv=time.strptime(dateSup,"%Y%m%d%H%M%S")
                    dateSup= time.strftime("%Y-%m-%dT%H:%M:%SZ",conv)
                    dateSup = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')

                    streamer = NameSmooth[12:18]
                    dicsmooth = manifest.getAttribSmoothStreamingMedia()
                    dic["measurement"]="SmoothStreamingMedia"
                    fieldS = {}
                    dicsmooth["commande"] = commande
                    dicsmooth["profil"] = profil
                    dicsmooth["streamer"] = noeud
                    fieldS["sap"] = int(random.randint(1, 9999))
                    for key, valeur in dicsmooth.items():            
                        if regex.match(valeur) is None:
                            #Le nbre est entier
                            fieldS[key] = int(valeur)
                            del dicsmooth[key]
                    dic["tags"]= dicsmooth
                    dic["time"] = dateSup
                    dic["fields"] = fieldS
                    json_bodyCATCHUP.append(dic)
                    
                    listStrmVid = manifest.getAttribStreamIndex("video")
                    for eStream in listStrmVid:
                        fieldS = {}
                        fieldS["sap"] = int(random.randint(1, 9999))
                        dic ={}
                        dic["measurement"]="StreamIndex"
                        eStream["commande"] = commande
                        eStream["profil"] = profil
                        eStream["streamer"] = noeud
                        for key, valeur in eStream.items():            
                            if regex.match(valeur) is None:
                                #Le nbre est entier
                                
                                fieldS[key] = int(valeur)
                                del eStream[key]
                        dic["tags"]= eStream
                        dic["time"] = dateSup
                        dic["fields"] = fieldS
                        json_bodyCATCHUP.append(dic)
                    listStrmAudio = manifest.getAttribStreamIndex("audio")
                    for eStream in listStrmAudio:
                        dic ={}
                        dic["measurement"]="StreamIndex"
                        eStream["commande"] = commande
                        eStream["profil"] = profil
                        eStream["streamer"] = noeud
                        fieldS = {}
                        fieldS["sap"] = int(random.randint(1, 9999))
                        for key, valeur in eStream.items():            
                            if regex.match(valeur) is None:
                                #Le nbre est entier
                                fieldS[key] = int(valeur)
                                del eStream[key]
                        dic["tags"]= eStream
                        dic["time"] = dateSup
                        dic["fields"] = fieldS
                        json_bodyCATCHUP.append(dic)
                    listQltVid = manifest.getQualityLevelAttribute("video")
                    for eqlty in listQltVid:
                        dic ={}
                        dic["measurement"]="QualityLevels"
                        eqlty["commande"] = commande
                        eqlty["profil"] = profil
                        eqlty["streamer"] = noeud
                        eqlty["typeStream"] = "video"
                        fieldS = {}
                        fieldS["sap"] = int(random.randint(1, 9999))
                        for key, valeur in eqlty.items():            
                            if regex.match(valeur) is None:
                                #Le nbre est entier
                                #print ("Faux")
                                if valeur !='':
                                    fieldS[key] = int(valeur)
                                    del eqlty[key]
                        dic["tags"]= eqlty
                        dic["time"] = dateSup
                        dic["fields"] = fieldS
                        json_bodyCATCHUP.append(dic)
                    
                    listQltAud = manifest.getQualityLevelAttribute("audio")
                    for eqltyAud in listQltAud:
                        dic ={}
                        dic["measurement"]="QualityLevels"
                        eqltyAud["typeStream"] = "audio"
                        eqltyAud["commande"] = commande
                        eqltyAud["profil"] = profil
                        eqltyAud["streamer"] = noeud
                        fieldSAud = {}
                        fieldSAud["sap"] = int(random.randint(1, 9999))
                        for cle, valeur in eqltyAud.items():           
                            if regex.match(valeur) is None:
                                #Le nbre est entier
                                #print ("Faux")
                                if valeur !='':
                                    fieldSAud[cle] = int(valeur)
                                    del eqltyAud[cle]
                        dic["tags"]= eqltyAud
                        dic["time"] = dateSup
                        dic["fields"] = fieldSAud
                        json_bodyCATCHUP.append(dic)
                        
                    listChunk = manifest.getChunksAttribute("video","t")
                    fieldChunk = {}
                    dic ={}
                    tagsChunk={}
                    tagsChunk["commande"] = commande
                    tagsChunk["profil"] = profil
                    tagsChunk["streamer"] = noeud
                    dic["measurement"]="Chunks"
                    tagsChunk["typechunk"] = "video"
                    for echunk in listChunk:
                        fieldChunk["t"] = int(echunk)
                        fieldChunk["sap"] = int(random.randint(1, 9999))
                           
                    dic["tags"]= tagsChunk
                    dic["time"] = dateSup
                    dic["fields"] = fieldChunk
                    json_bodyCATCHUP.append(dic)
                    listChunk = manifest.getChunksAttribute("audio","t")
                    fieldChunk = {}
                    dic ={}
                    tagsChunk={}
                    dic["measurement"]="Chunks"
                    tagsChunk["typechunk"] = "audio"
                    tagsChunk["commande"] = commande
                    tagsChunk["profil"] = profil
                    tagsChunk["streamer"] = noeud
                    for echunk in listChunk:
                        fieldChunk["t"] = int(echunk)
                        fieldChunk["sap"] = int(random.randint(1, 9999))
                           
                    dic["tags"]= tagsChunk
                    dic["time"] = dateSup
                    dic["fields"] = fieldChunk
                    json_bodyCATCHUP.append(dic)
                    #result = client.query('select value from cpu_load_short;')
                    #print("Result: {0}".format(result))
                    #time.sleep(10)
            #End for
            
            """
            Création d'une Route pour faire du SMOOTH
            """
            routeMSS = Route()
            """
            On définit le type de fichier Manifest à recupèrer
            """
            mss = routeMSS.getManifest("LIVE", "smooth")
            #routeMSS.download(mss)
            """
            Idem pour DASH !
            """
            routeDASH = Route()
            dash = routeDASH.getManifest("LIVE", "dash")
            #routeDASH.download(dash)
            """
            Idem pour HLS !
            """
            routeHLS = Route()
            hls = routeHLS.getManifest("LIVE", "hls")
            #routeHLS.download(hls)
            print ("\n")
            """
            On choisit les 4 derniers fichiers à traiter dans une LISTE
            """
            listeMSS  = routeMSS.getLastXMLFile("/home/adama/NetBeansProjects/ABSTRACT1_0/abstract1_0/manifests/dynamic/MSS")
            listeDASH = routeDASH.getLastXMLFile("/home/adama/NetBeansProjects/ABSTRACT1_0/abstract1_0/manifests/dynamic/DASH")
            listeHLS  = routeHLS.getLastXMLFile("/home/adama/NetBeansProjects/ABSTRACT1_0/abstract1_0/manifests/dynamic/HLS")
            """
            TRAITEMENT DE CHAQUE FICHIER DE MES DIFFÉRENTES LISTES
            """
            for element in listeMSS:
                manifest = DataManifestMSS(element)
                """
                Validation du fichier Manifest avec le schéma donné
                """
                if manifest.validManifest()== True:
                    json_bodyLIVE = []
                    dic={}
                    
                    """ Nom du fichier dans le système """
                    NameSmooth = element.split("/")
                    NameSmooth= NameSmooth[len(NameSmooth)-1]
                    listdetails = NameSmooth.split("_")
                    dateSup = listdetails[len(listdetails)-1]
                    noeud = listdetails[len(listdetails)-2]
                    profil = listdetails[len(listdetails)-3]
                    commande = listdetails[len(listdetails)-4]
                    conv=time.strptime(dateSup,"%Y%m%d%H%M%S")
                    dateSup= time.strftime("%Y-%m-%dT%H:%M:%SZ",conv)
                    dateSup = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
                    streamer = NameSmooth[12:18]
                    
                    dicsmooth = manifest.getAttribSmoothStreamingMedia()
                    dic["measurement"]="SmoothStreamingMedia"
                    fieldS = {}
                    #Données bitrate 
                    fieldS["sap"] = int(random.randint(1, 9999))
                    dicsmooth["commande"] = commande
                    dicsmooth["profil"] = profil
                    dicsmooth["streamer"] = noeud
                    for key, valeur in dicsmooth.items():            
                        if regex.match(valeur) is None:
                            #Le nbre est entier
                            fieldS[key] = int(valeur)
                            del dicsmooth[key]
                    dic["tags"]= dicsmooth
                    dic["time"] = dateSup
                    dic["fields"] = fieldS
                    json_bodyLIVE.append(dic)
                    
                    listStrmVid = manifest.getAttribStreamIndex("video")
                    for eStream in listStrmVid:
                        fieldS = {}
                        fieldS["sap"] = int(random.randint(1, 9999))
                        dic ={}
                        dic["measurement"]="StreamIndex"
                        eStream["commande"] = commande
                        eStream["profil"] = profil
                        eStream["streamer"] = noeud
                        for key, valeur in eStream.items():            
                            if regex.match(valeur) is None:
                                #Le nbre est entier
                                
                                fieldS[key] = int(valeur)
                                del eStream[key]
                        dic["tags"]= eStream
                        dic["time"] = dateSup
                        dic["fields"] = fieldS
                        json_bodyLIVE.append(dic)
                    listStrmAudio = manifest.getAttribStreamIndex("audio")
                    for eStream in listStrmAudio:
                        dic ={}
                        dic["measurement"]="StreamIndex"
                        eStream["commande"] = commande
                        eStream["profil"] = profil
                        eStream["streamer"] = noeud
                        fieldS = {}
                        fieldS["sap"] = int(random.randint(1, 9999))
                        for key, valeur in eStream.items():            
                            if regex.match(valeur) is None:
                                #Le nbre est entier
                                fieldS[key] = int(valeur)
                                del eStream[key]
                        dic["tags"]= eStream
                        dic["time"] = dateSup
                        dic["fields"] = fieldS
                        json_bodyLIVE.append(dic)
                    listQltVid = manifest.getQualityLevelAttribute("video")
                    for eqlty in listQltVid:
                        dic ={}
                        dic["measurement"]="QualityLevels"
                        eqlty["commande"] = commande
                        eqlty["profil"] = profil
                        eqlty["streamer"] = noeud
                        eqlty["typeStream"] = "video"
                        fieldS = {}
                        fieldS["sap"] = int(random.randint(1, 9999))
                        for key, valeur in eqlty.items():            
                            if regex.match(valeur) is None:
                                #Le nbre est entier
                                #print ("Faux")
                                if valeur !='':
                                    fieldS[key] = int(valeur)
                                    del eqlty[key]
                        dic["tags"]= eqlty
                        dic["time"] = dateSup
                        dic["fields"] = fieldS
                        json_bodyLIVE.append(dic)
                    
                    listQltAud = manifest.getQualityLevelAttribute("audio")
                    for eqltyAud in listQltAud:
                        dic ={}
                        dic["measurement"]="QualityLevels"
                        eqltyAud["typeStream"] = "audio"
                        eqltyAud["commande"] = commande
                        eqltyAud["profil"] = profil
                        eqltyAud["streamer"] = noeud
                        fieldSAud = {}
                        fieldSAud["sap"] = int(random.randint(1, 9999))
                        for cle, valeur in eqltyAud.items():           
                            if regex.match(valeur) is None:
                                #Le nbre est entier
                                #print ("Faux")
                                if valeur !='':
                                    fieldSAud[cle] = int(valeur)
                                    del eqltyAud[cle]
                        dic["tags"]= eqltyAud
                        dic["time"] = dateSup
                        dic["fields"] = fieldSAud
                        json_bodyLIVE.append(dic)
                        
                    listChunk = manifest.getChunksAttribute("video","t")
                    fieldChunk = {}
                    dic ={}
                    tagsChunk={}
                    tagsChunk["commande"] = commande
                    tagsChunk["profil"] = profil
                    tagsChunk["streamer"] = noeud
                    dic["measurement"]="Chunks"
                    tagsChunk["typechunk"] = "video"
                    for echunk in listChunk:
                        fieldChunk["t"] = int(echunk)
                        fieldChunk["sap"] = int(random.randint(1, 9999))
                           
                    dic["tags"]= tagsChunk
                    dic["time"] = dateSup
                    dic["fields"] = fieldChunk
                    json_bodyLIVE.append(dic)
                    listChunk = manifest.getChunksAttribute("audio","t")
                    fieldChunk = {}
                    dic ={}
                    tagsChunk={}
                    dic["measurement"]="Chunks"
                    tagsChunk["typechunk"] = "audio"
                    tagsChunk["commande"] = commande
                    tagsChunk["profil"] = profil
                    tagsChunk["streamer"] = noeud
                    for echunk in listChunk:
                        fieldChunk["t"] = int(echunk)
                        fieldChunk["sap"] = int(random.randint(1, 9999))
                           
                    dic["tags"]= tagsChunk
                    dic["time"] = dateSup
                    dic["fields"] = fieldChunk
                    json_bodyLIVE.append(dic)
                                       
                    #print (json_body)
                    client = InfluxDBClient('148.60.11.196', 8086, 'admin', 'admin', 'abstract')
                    #client.create_database('example')
                    client.write_points(json_bodyLIVE)
                    client.write_points(json_bodyCATCHUP)
                    #result = client.query('select value from cpu_load_short;')
                    #print("Result: {0}".format(result))
                    #time.sleep(10)
            #END FOR LIVE
            #i = i +1
            