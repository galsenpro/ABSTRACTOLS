#!/usr/bin/python
#-*- coding: utf-8 -*-

import glob
import os
import json
import re
from ipykernel import comm
json_body = []
measurement={}
tags ={}
tagsSmooth ={}
tagsStreamIndex={}
tagsStreamIndexAudio= {}
regex = re.compile(r"[0-9]*[a-zA-Z]+[0-9]*")

fields={}

class Traiter:
    
    def __init__(self, manifestJSONFile):
        #self.manifestJSONFile = manifestJSONFile
        self.manifestJSONFile = manifestJSONFile
        self.configSMOOTH = json.loads(open(str(self.manifestJSONFile)).read())
        self.dicoSmooth = self.configSMOOTH['SmoothStreamingMedia']
        self.listeQltyGenerated = self.configSMOOTH['SmoothStreamingMedia']['StreamIndex']
        self.listStreamIndex = self.configSMOOTH['SmoothStreamingMedia']['StreamIndex']
        self.listStreamIndexChunks = self.configSMOOTH['SmoothStreamingMedia']['StreamIndex']
        self.listpods = []
    
    def genSmoothTable(self, nameCollection, timefile,commande, profil, noeud):
        try:
            json_body = []
            fieldS = {}
            tags = {}
            dic = {}
            #configSMOOTH = json.loads(open(str(self.manifestJSONFile)).read())
            #dicoSmooth = configSMOOTH['SmoothStreamingMedia']
            self.dicoSmooth["commande"] = commande
            self.dicoSmooth["profil"] = profil
            self.dicoSmooth["noeud"] = noeud
            del self.dicoSmooth['StreamIndex']
            #print(dicoSmooth)
            for key, valeur in self.dicoSmooth.items(): 
                if str(type(valeur)) != "<type 'list'>":          
                    if regex.match(valeur) is None:
                        if valeur !='':
                            fieldS[key] = int(valeur)
                            del self.dicoSmooth[key]
                dic["tags"]= self.dicoSmooth
                dic["fields"] = fieldS
                dic["time"]=timefile
                dic["measurement"]= str(nameCollection)
            json_body.append(dic)
            #print(json_body)
            return json_body
        except Exception as x:
            print(x)
    
    
    
    def genStreamIndexTable(self, nameCollection, timefile,commande, profil, noeud):
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
                    for key, valeur in element.items():           
                        if regex.match(valeur) is None:
                            if valeur !='':
                                fieldS[key] = int(valeur)
                                del element[key]
                    dic["tags"]= element
                    dic["fields"] = fieldS
                    dic["time"]=timefile
                    dic["measurement"]= str(nameCollection)
            json_body.append(dic)
            #print(json_body)
            return json_body
        except Exception as x:
            print(x)  
    
    
    def genQualityTable(self,nameCollection, timefile,commande, profil, noeud):
        try:
            json_body = []
            for element in self.listeQltyGenerated:
                qlt = element.get('QualityLevel')
                if str(type(qlt)) == "<type 'list'>":
                    #print(qlt)
                    for eqlty in qlt:
                        fieldS = {}
                        tags = {}
                        dic = {}
                        eqlty["commande"] = commande
                        eqlty["profil"] = profil
                        eqlty["noeud"] = noeud
                        for key, valeur in eqlty.items():            
                            if regex.match(valeur) is None:
                                if valeur !='':
                                    fieldS[key] = int(valeur)
                                    del eqlty[key]
                        dic["tags"]= eqlty
                        dic["fields"] = fieldS
                        dic["time"]=timefile
                        dic["measurement"]=str(nameCollection)
                    json_body.append(dic)
                else:
                    if str(type(qlt)) == "<type 'dict'>":
                        #print(qlt)
                        eqlty = {}
                        fieldS = {}
                        tags = {}
                        dic = {}
                        qlt["commande"] = commande
                        qlt["profil"] = profil
                        qlt["noeud"] = noeud 
                        for key, valeur in qlt.items():          
                            if regex.match(valeur) is None:
                                if valeur !='':
                                    fieldS[key] = int(valeur)
                                    del qlt[key]
                        dic["tags"]= qlt
                        dic["fields"] = fieldS
                        dic["time"]=timefile
                        dic["measurement"]=str(nameCollection)
                        json_body.append(dic)
            #print(json_body)
            return json_body
        except Exception as x:
            print(x)
    
    def genChunksTable(self, nameCollection, timefile,commande, profil, noeud):
        try:
            json_body = []
            for element in self.listStreamIndexChunks:
                fieldS = {}
                tags = {}
                dic = {}
                tags["Type"] = element.get('Type')
                tags["commande"] = commande
                tags["profil"] = profil
                tags["noeud"] = noeud
                fieldS["duree"] = int(element['c'][0].get('t'))
                dic["tags"]= tags
                dic["fields"] = fieldS
                dic["time"]=timefile
                dic["measurement"]= str(nameCollection)
                json_body.append(dic)
            #print(json_body)
            return json_body
        except Exception as x:
            print(x)
            
    def generateBody(self,timefile,commande, profil, noeud):
        try:
            ql= self.genQualityTable('QualityLevel',timefile,commande, profil, noeud)
            chunk = self.genChunksTable('Chunks',timefile,commande, profil, noeud)
            strm = self.genStreamIndexTable('StreamIndex',timefile,commande, profil, noeud)
            mss = self.genSmoothTable('SmoothMediaStream',timefile,commande, profil, noeud)
            flux = mss + ql + chunk + strm
            print(json.dumps(flux))
            return json.dumps(flux)
        except Exception as x:
            print(x)
"""                 
test = Traiter('/home/adama/Bureau/traitement/Arte_LIVESMOOTH_NODEA1_20170228132851')

print('--------Flux.....')
test.generateBody('2017-01-23T14:31:16Z','LIVE','SMOOTH','NODEouPOD')

"""