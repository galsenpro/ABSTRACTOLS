#!/usr/bin/python
#-*- coding: utf-8 -*-

import urllib
import requests
from requests.exceptions import HTTPError
class HLS:
    def __init__(self, originLink,  HLSFile=""):
        self.originLink = originLink
        self.HLSFile = HLSFile
        self.dico = {}
        
    def getInfosHls(self):
        try:
            levelsList = []
            BPVideoList = []
            RESOVidList = []
            CODECVidList = []
            iframesList= []
            BPAudioList = []
            CODECAudList = []
            print("Fichier à traiter : " + self.HLSFile)
            file = open(self.HLSFile, "r")
            lines = file.readlines()
            for line in lines:
                if line.find('EXT-X-STREAM-INF:PROGRAM') != -1:
                    """ La Bande passante de la vidéo """
                    deb= line.find('BANDWIDTH=') +10 
                    fin = line.find(',CODECS', deb)
                    BPVideo = line[deb:fin]
                    """ Le CODEC de la vidéo """
                    deb= line.find('CODECS="') +8
                    fin = line.find('",', deb)
                    CodecVideo = line[deb:fin]
                    """ La Résolution de la vidéo """
                    deb= line.find('RESOLUTION=') +11
                    fin = line.find('\n', deb)
                    ResolVideo = line[deb:fin]
                    
                    BPVideoList.append(BPVideo)
                    CODECVidList.append(CodecVideo)
                    RESOVidList.append(ResolVideo)
                    #lines.remove(line)
            """ Les Levels """
            for level in lines:
                if level.find("/Level(") != -1:
                    deb= level.find('index=') +1
                    fin = level.find('\n', deb)
                    link = level[deb:fin]
                    
                    levelsList.append(link)
                    #lines.remove(level)
                    
            """ Les Iframes """
            for iframe in lines:
                if iframe.find("/Iframe(") != -1:
                    deb= iframe.find('BANDWIDTH=') +10 
                    fin = iframe.find(',CODECS', deb)
                    BPAudio = iframe[deb:fin]
                    
                    
                    deb= iframe.find('CODECS="') +8
                    fin = iframe.find('",URI', deb)
                    CodecAudio = iframe[deb:fin]
                    
                    deb = iframe.find('URI="index') +5 
                    fin = iframe.find('Z"', deb)
                    link = iframe[deb:fin]+"Z"
                    
                    BPAudioList.append(BPAudio)
                    CODECAudList.append(CodecAudio)
                    iframesList.append(link)
            i = 0
            contenthls = []
            while i < len(levelsList) :
                bodyhls = {}
                bodyhls["bandwithVid"] = int(BPVideoList[i])
                bodyhls["codecVideo"] = str(CODECVidList[i])
                bodyhls["resolution"] = str(RESOVidList[i])
                bodyhls["level"] = str(levelsList[i])
                bodyhls["iframe"] = str(iframesList[i])
                bodyhls["bandwithAudio"] = int(BPAudioList[i])
                bodyhls["codecAudio"] = str(CODECAudList[i])
                contenthls.append(bodyhls)
                i = i +1
            print(contenthls)
            return contenthls
        except IOError:
            print("Fichier HLS introuvable ! ")
        except Exception as x:
            print(x)
                
    """ Retourne le prefix du Lien HLS - Pods et Streamers"""
    def getprefixOnOriginLink(self):
        try:
            print("Origin Link :" + self.originLink)
            prefix = self.originLink.split('10.m3u8')[0]
            print(prefix)
            return str(prefix)
        except Exception as x:
            print(x)
    """ Retourne le lien pour Obtenir le Chunk de chaque Level"""
    def getAllLinkOfChunkByLevelList(self, levelList):
        try:
            lienChunkList = []
            for levelElem in levelList:
                lienChunk = str(self.getprefixOnOriginLink())+str(levelElem)
                lienChunkList.append(lienChunk)
            return lienChunkList
        except Exception as x:
            print(x)
    """
        - Je recupère le lien du Chunk
        - Je garde la valeur du Level, l'adresse du Pod ou du Streamer,
            le start et le end
    """
    def downloadChunks(self, LinkOfChunks, folderOfChunk , filenameOfChunk):
        try:
            print("Téléchargement des Chunks ...")
            path = str(folderOfChunk)+str(filenameOfChunk)
            urllib.urlretrieve (str(LinkOfChunks), path)
            print(path)
            return str(path)
        except URLError as e:
            if e.code == 404:
                print ("4 0 4")
                return "4 0 4"
            else:
                print ("%s" % e)
                return "%s" % e
        except Exception as x:
            print(x)
            return x
    
    def createFieldOfChunkFied(self, chunkFile, commande, mode, start, end, noeud, originUrl, level, levelURL):
        try:
            print("Creating FieldsJSON for DB ....")
            levelsList= []
            print("Fichier des Chunks à traiter : " + chunkFile)
            file = open(chunkFile, "r")
            lines = file.readlines()
            #print(lines)
            for line in lines:
                if line.find("/Level(") != -1:
                    levelsList.append(line)
            print(levelsList)
            return levelsList
        except IOError:
            print("Fichier Manifest introuvable ! ")
            
        except Exception as x:
            print(x)
        
#http://192.168.134.68:5555/shls/LIVE$CH_4/10.m3u8?start=2017-03-06T06:18:08Z&end=2017-03-06T10:18:08Z&device=HLS_LOW
hls = HLS("http://192.168.134.68:5555/shls/LIVE$CH_4/10.m3u8?start=2017-03-06T06:18:08Z&end=2017-03-06T10:18:08Z&device=HLS_LOW", "contentOne.m3u8")
pref = hls.getprefixOnOriginLink()
listL = hls.getInfosHls()

"""
lienC = hls.getAllLinkOfChunkByLevelList(listL)
for el in lienC:
    print(el)
    hls.downloadChunks(el, "/home/kirikou/Levels/", "Level"+ str(lienC.index(str(el))))
"""

    