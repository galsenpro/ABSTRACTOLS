#!/usr/bin/python
# -*- coding: utf-8 -*-

from influxdb import InfluxDBClient
import glob
import os
import json
import re

# from ipykernel import comm
json_body = []
measurement = {}
tags = {}
tagsSmooth = {}
tagsStreamIndex = {}
tagsStreamIndexAudio = {}
regex = re.compile(r"[0-9]*[a-zA-Z]+[0-9]*")

fields = {}


class Traiter:
    """ Initialisation de la Class de Traitement des Manifests JSON => InfluxDB """

    def __init__(self, manifestJSONFile, hostInflux="192.168.134.122",
                 portInflux=8086, userInflux="admin", passwdInflux="admin", dbInflux="abstract1"):

        self.manifestJSONFile = manifestJSONFile
        # print(self.manifestJSONFile)
        self.configSMOOTH = json.loads(open(str(self.manifestJSONFile)).read())
        self.dicoSmooth = self.configSMOOTH["SmoothStreamingMedia"]
        self.listeQltyGenerated = self.configSMOOTH["SmoothStreamingMedia"]["StreamIndex"]
        self.listStreamIndex = self.configSMOOTH["SmoothStreamingMedia"]["StreamIndex"]
        self.listStreamIndexChunks = self.configSMOOTH["SmoothStreamingMedia"]["StreamIndex"]
        self.listpods = []
        # Données de le base de données InfluxDB
        self.hostInflux = hostInflux
        self.portInflux = portInflux
        self.userInflux = userInflux
        self.passwdInflux = passwdInflux
        self.dbInflux = dbInflux

    """Génération de la Table du SmoothMediaStream"""
    """
        REMARQUE : Ajouter le status de la requete dans la remontée 
        - 1 : ajouter un paramètre status (Ex : nomParametre = status)
        - 2 : self.dicoSmooth["status"] = status
    """
    def genSmoothTable(self, nameCollection, timefile, commande, profil, noeud, chaine, status = None):
        try:
            json_body = []
            fieldS = {}
            tags = {}
            dic = {}
            self.dicoSmooth["commande"] = commande
            self.dicoSmooth["profil"] = profil
            self.dicoSmooth["noeud"] = noeud
            self.dicoSmooth["chaine"] = chaine
            #self.dicoSmooth["status"] = status
            del self.dicoSmooth["StreamIndex"]
            for key, valeur in self.dicoSmooth.items():
                if str(type(valeur)) != "<type 'list'>":
                    if regex.match(valeur) is None:
                        if valeur != "":
                            fieldS[key] = int(valeur)
                            del self.dicoSmooth[key]
                dic["tags"] = self.dicoSmooth
                dic["fields"] = fieldS
                dic["time"] = timefile
                #Nom de la table dans InfluxDB
                dic["measurement"] = str(nameCollection)
            json_body.append(dic)
            return json_body
        except Exception as x:
            print(x)

    """ Génération de la Table du StreamIndex"""

    def genStreamIndexTable(self, nameCollection, timefile, commande, profil, noeud, chaine, status = None):
        try:
            json_body = []
            for element in self.listStreamIndex:
                if str(type(element)) == "<type 'dict'>":
                    del element["QualityLevel"]
                    del element["c"]
                    fieldS = {}
                    tags = {}
                    dic = {}
                    element["commande"] = commande
                    element["profil"] = profil
                    element["noeud"] = noeud
                    element["chaine"] = chaine
                    for key, valeur in element.items():
                        if regex.match(valeur) is None:
                            if valeur != "":
                                fieldS[key] = int(valeur)
                                del element[key]
                    dic["tags"] = element
                    dic["fields"] = fieldS
                    dic["time"] = timefile
                    dic["measurement"] = str(nameCollection)
            json_body.append(dic)
            return json_body
        except Exception as x:
            print(x)

    """ Génération de la Table du QualityLevel"""

    def genQualityTable(self, nameCollection, timefile, commande, profil, noeud, chaine):
        try:
            json_body = []
            for element in self.listeQltyGenerated:
                qlt = element.get("QualityLevel")
                if str(type(qlt)) == "<type 'list'>":
                    for eqlty in qlt:
                        fieldS = {}
                        tags = {}
                        dic = {}
                        eqlty["commande"] = commande
                        eqlty["profil"] = profil
                        eqlty["noeud"] = noeud
                        eqlty["chaine"] = chaine
                        for key, valeur in eqlty.items():
                            if regex.match(valeur) is None:
                                if valeur != "":
                                    fieldS[key] = int(valeur)
                                    del eqlty[key]
                        dic["tags"] = eqlty
                        dic["fields"] = fieldS
                        dic["time"] = timefile
                        dic["measurement"] = str(nameCollection)
                    json_body.append(dic)
                else:
                    if str(type(qlt)) == "<type 'dict'>":
                        eqlty = {}
                        fieldS = {}
                        tags = {}
                        dic = {}
                        qlt["commande"] = commande
                        qlt["profil"] = profil
                        qlt["noeud"] = noeud
                        for key, valeur in qlt.items():
                            if regex.match(valeur) is None:
                                if valeur != "":
                                    fieldS[key] = int(valeur)
                                    del qlt[key]
                        dic["tags"] = qlt
                        dic["fields"] = fieldS
                        dic["time"] = timefile
                        dic["measurement"] = str(nameCollection)
                        json_body.append(dic)
            return json_body
        except Exception as x:
            print(x)

    """ Génération de la Table des Chunks """

    def genChunksTable(self, nameCollection, timefile, commande, profil, noeud, chaine):
        try:
            json_body = []
            for element in self.listStreamIndexChunks:
                fieldS = {}
                tags = {}
                dic = {}
                tags["Type"] = element.get("Type")
                tags["commande"] = commande
                tags["profil"] = profil
                tags["noeud"] = noeud
                tags["chaine"] = chaine
                fieldS["duree"] = int(element["c"][0].get("t"))
                dic["tags"] = tags
                dic["fields"] = fieldS
                dic["time"] = timefile
                dic["measurement"] = str(nameCollection)
                json_body.append(dic)
            return json_body
        except Exception as x:
            print(x)

    """Génération JsonBody( fusion des Fields pour InfluxDB """

    def generateFlux(self, timefile, commande, profil, noeud, chaine):
        try:
            ql = self.genQualityTable("QualityLevel", timefile, commande, profil, noeud, chaine)
            chunk = self.genChunksTable("Chunks", timefile, commande, profil, noeud, chaine)
            strm = self.genStreamIndexTable("StreamIndex", timefile, commande, profil, noeud, chaine)
            mss = self.genSmoothTable("SmoothMediaStream", timefile, commande, profil, noeud, chaine)
            flux = mss + ql + chunk + strm
            # print("Le Body_Flux generated : " + str(flux))
            return flux
        except Exception as x:
            print(x)

    def pushToDB(self, flux):
        try:
            # print("Connexion à InfluxDB ...")
            client = InfluxDBClient(self.hostInflux, self.portInflux, self.userInflux, self.passwdInflux, self.dbInflux)
            # client.create_database("example")
            client.write_points(flux)
            # print("Insertion réussie")
            contenu = str(flux)
            contenu = contenu.replace("'", "\"")
            contenu = contenu.replace("u\"", "\"")
            print(contenu)
            fichier = open(str(self.manifestJSONFile), 'w')
            fichier.write(contenu)
            fichier.close()
        except Exception as x:
            print(x)


"""
test = Traiter("/home/kirikou/ABSTRACT/abstract1_0/manifests/dynamic/MSS/Live/Arte_LIVESMOOTH_NODEA1_20170316150107")
bodyJSON = test.generateFlux("2017-03-07T14:01:11", "commande", "profil", "noeud")
test.pushToDB(bodyJSON)
"""
