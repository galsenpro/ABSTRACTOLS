#!/usr/bin/python
#-*- coding: utf-8 -*-

import random
from lxml import etree
import lxml
import datetime
import time
from operator import or_
import urllib
import requests
import xmltodict
import errno
import urllib3
from traiter import *
import os
class RouteConfig:
    def __init__(self, fileConfig = "/home/kirikou/ABSTRACT/abstract1_0/configs/configurations.json"):
        try:
            self.config = json.loads(open(fileConfig).read())
            self.listpods = []
            self.liststrms = []
            self.dictStrms = {"namepod": self.liststrms}
            self.listChaine = []
            self.dictChannels = {"adrStrm": self.listChaine}
            self.listpaterns = ["pat1", "pat2"]
            self.typeFile = "/Manifest"
            self.dictEmail = {}
            self.listAdr = []
        except Exception as x:
            print(x)
    """Recupére le protocole depuis la config """
    def getProtocole(self):
        try:
            return self.config["protocole"]
        except Exception as x:
            print(x)
            self.createLogFile(x)

    """Recupére le port depuis la config """
    def getPort(self):
        try:
            return self.config["port"]
        except Exception as x:
            self.createLogFile(x)

    """Recupére les répertoire de stockage des Manifests"""
    def getFolder(self, commande, mode):
        try:
            attribut = str(commande)+'folder'+str(mode)
            return self.config[attribut]
        except Exception as x:
            print(x)
            self.createLogFile(x)

    """Recupére le dossier des logs """
    def getLogFolder(self):
        try:
            return self.config["logdirectory"]
        except Exception as x:
            print(x)
            self.createLogFile(x)

    """Recupére le nom du prefix Lof """
    def getLogPrefix(self):
        try:
            return self.config["logprefixname"]
        except Exception as x:
            print(x)
            self.createLogFile(x)

    """Recupére l'intervalle de tests """
    def getIntervalle(self):
        try:
            return self.config["intervalle"]
        except Exception as x:
            print(x)
            self.createLogFile(x)

    """Recupére l'Email pour les alertes """
    def getEmailFrom(self):
        try:
            print(self.config["emailFrom"])
            return self.config["emailFrom"]
        except Exception as x:
            print(x)
            self.createLogFile(x)

    """For the SMS service """
    def getSmsFrom(self):
        try:
            return self.config["smsFrom"]
        except Exception as x:
            print(x)
            self.createLogFile(x)

    """Pour le Timeout """
    def getTimeoutTest(self):
        for timeO in self.tree.xpath("/configs/timeout"):
            return timeO.text

    """Retourne une liste de Pods avec ses différents attributs"""
    def getPods(self):
        try:
            return self.config["configs"]["pods"]["pod"]
        except Exception as x:
            print(x)
            self.createLogFile(x)

    """Le fichier xsd du SMOOTH """
    def getSmoothSchema(self):
        try:
            return self.config["schemasmooth"]
        except Exception as x:
            print(x)
            self.createLogFile(x)

    """"Le schéma DASH """
    def getDashSchema(self):
        try:
            return self.config["schemadash"]
        except Exception as x:
            print(x)
            self.createLogFile(x)

    """Les attributs des différents Pods """
    def getAttributeOfPod(self, attribute):
        self.listpods =[]
        try:
            list = self.config["configs"]["pods"]["pod"]
            for pod in list:
                self.listpods.append(pod.get(str(attribute)))
            return self.listpods
        except Exception as x:
            print(x)
            self.createLogFile(x)

    """Retourne la valeur de chaque attribut d'un Pod donné en paramètre"""

    def getValAttributeByPod(self,namePod, attribute):
        try:
            for element in self.config["configs"]["pods"]["pod"]:
                if element.get("name") == str(namePod):
                    return element.get(str(attribute))
        except Exception as x:
            print(x)
            self.createLogFile(x)

    """ Retourne la liste des attributs de Streamers ou Chaines qui sont dans un Pod"""

    def getValAttributeStrmAndChannel(self,listStrm, attribute):
        listElements = []
        try:
            for str in listStrm:
                listElements.append((str.get(str(attribute))))
            return listElements
        except Exception as x:
            print(x)
            self.createLogFile(x)

    """Retourne la liste des Streamers Suivant un Pod bien défini """

    def getListStreamers(self, listDicoStr, attribute):
        malisteStr = []
        try:
            for element in listDicoStr:
                malisteStr.append(element.get(str(attribute)))
            return malisteStr
        except Exception as x:
            print(x)
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
            print(x)
            self.createLogFile(x)
    """  Ajout d'un nouveau   """
    def setPatern(self):
        self.dictpaterns["pat1"] = self.dictpods
        self.dictpaterns["pat2"] = self.dictstrms
        return self.dictpaterns

    """ Retourne un attribut d'un Mode dans le fichier de configuration """

    def getValAttributeOfMode(self,lemode, attribute):
        try:
            return self.config["configs"]["modes"][str(lemode)][str(attribute)]
        except Exception as x :
            print(x)
            self.createLogFile(x)

    """ Retourne un attribut d'une Commande dans le fichier de configuration """

    def getValAttributeOfCommands(self,lacommande, attribute):
        try:
            return self.config["configs"]["commands"][str(lacommande)][str(attribute)]
        except Exception as x :
            print(x)
            self.createLogFile(x)

    """ Exécution du Partern 1 : Routage par les Pods """

    def makePaternOne(self,commande = "catchup", mode="smooth" , *listeChannelsDistinctsPods):
        try:
            """ Mon dictionnaire de flux pour InfluxDB """
            monflux =  {}
            monflux["pattern"] = "patternOne"
            monflux["commande"] = str(commande)
            monflux["mode"] = str(mode)
            monflux["timestamp"] = str(datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S%ZZ"))
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
            
            
            #Jusqu'ici je ne fais que créer les URL statiques
            mesManifests = []
            """Je crée un dico qui contient les infos liées à ce manifest"""
            for pod in listPods:
                nompod = pod[5:9]
                """Chaine liée au pod"""
                chs = self.getValAttributeByPod(str(nompod), "channels")
                liste = []
                taille = len(chs.get("channel"))
                i = 0
                while i < taille:
                    """ Dictionnaire qui contient l'URL et tous les paramètres liés à cet URL"""
                    dicomanifest =  {}
                    chaine = chs.get("channel")[i].get("nom")
                    monUrl = protocole+"://"+ pod +":"+port+"/"+abr+"/LIVE$"+chaine+"/"+frag+"."+suffix+self.typeFile+"?start="+startM+"&end="+endM+"&device="+dev
                    print(manifest)
                    dicomanifest["chaine"] = chaine
                    dicomanifest["noeud"] = pod
                    dicomanifest["start"] = str(startM)
                    dicomanifest["end"] = str(endM)
                    dicomanifest["manifestURL"] = monUrl
                    http = urllib3.PoolManager()
                    req = http.request('GET', str(monUrl))
                    # Attribut du statut de la requête Manifest (request = status)
                    dicomanifest["request"] = str(req.status)
                    #Ajouter du dictionnaire des infos du Pod dans la Liste Manifests
                    mesManifests.append(dicomanifest)
                    i = i+1
            """
            A la sortie de la boucle, j'aurai les infos de chaque Manifests dans une Liste Manifests
            J'affecte à présent ma Liste  manifest dans Dictionnaire de Flux
            """
            print(mesManifests)
            return mesManifests
            #monflux["manifests"] = mesManifests
            #return json.dumps(monflux)
        except Exception as x:
            print(x)

    """ Exécution du Patern 2 : Routage par les Streamers """

    def makePaternTwo(self,commande = "catchup", mode="smooth" , *listeChannelsDistinctsPods):
        try:
            """ Mon dictionnaire de flux pour ElasticSearch """
            monflux =  {}
            monflux["pattern"] = "patternTwo"
            monflux["commande"] = str(commande)
            monflux["mode"] = str(mode)
            monflux["timestamp"] = str(datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S%ZZ"))
            print("\n--PARTERN 2 : STREAMERS :  "+str(mode).upper()+" on "+str(commande).upper()+" ...\n")
            protocole   = self.getProtocole()
            port   = self.getPort()
            abr    = self.getValAttributeOfMode(str(mode), "staticabr")
            frag   = self.getValAttributeOfMode(str(mode), "fragment")
            suffix = self.getValAttributeOfMode(str(mode), "manifestsuffix")
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
            mesManifests = []
            for pod in listPods:
                podXStrm = self.getValAttributeByPod(str(pod), "streamer")
                chs = self.getValAttributeByPod(str(pod), "channels")
                liste = []
                taille = len(chs.get("channel"))
                i = 0
                while i < taille:
                    listAdress = self.getListStreamers(podXStrm, "address")
                    for adr in listAdress:
                        dicomanifest =  {}
                        chaine = chs.get("channel")[i].get("nom")
                        manifest = protocole+"://"+ adr +":"+port+"/"+abr+"/LIVE$"+chaine+"/"+frag+"."+suffix+self.typeFile+"?start="+startM+"&end="+endM+"&device="+dev
                        print(manifest)
                        dicomanifest["chaine"] = chaine
                        dicomanifest["noeud"] = adr
                        dicomanifest["start"] = str(startM)
                        dicomanifest["end"] = str(endM)
                        dicomanifest["manifestURL"] = manifest
                        http = urllib3.PoolManager()
                        req = http.request('GET', str(manifest))
                        dicomanifest["request"] = str(req.status)
                        mesManifests.append(dicomanifest)
                    i = i+1
                    """
                    A la sortie de la boucle, j'aurai les infos de chaque Manifests dans une Liste Manifests
                    J'affecte à présent ma Liste  manifest dans Dictionnaire de Flux
                    """
            print(mesManifests)
            return mesManifests
            #return json.dumps(monflux)
        except Exception as x:
            print(x)

    """ Exécution par choix aléatoire de PATERN """

    def threader(self,listPartern, listCommands, listModes):
        try:
            patern = random.choice(listPartern)
            commandchoisi = random.choice(listCommands)
            modechoisi = random.choice(listModes)
            flux = {}
            if str(patern).upper() == "PATERN1":
                """ Le flux est en ce moment juste un URL Manifest et les infos du Manifests sous forme de liste"""
                flux = self.makePaternOne(commandchoisi, modechoisi)
                for edict in flux:
                    tagsManifest = []
                    for cle, valeur in edict.items():
                        print(cle,valeur)
                        tagsManifest.append(valeur)
                        #tagsManifest[cle] = edict.get[cle]
                    noeud = str(tagsManifest[0])[5:9]
                    chaine = str(tagsManifest[3])
                    timeM= datetime.datetime.utcnow()
                    folder = str("manifests/"+ patern + "/" + commandchoisi + "/"+ modechoisi + "/" + noeud)
                    self.creatingFolder(folder)
                    file = folder + "/"+ tagsManifest[3]
                    print(file)
                    urllib.urlretrieve(tagsManifest[2], file )
                    time.sleep(10)
                    http = urllib3.PoolManager()
                    req = http.request('GET', str(tagsManifest[2]))
                    from xml.dom.minidom import parseString
                    try:
                        dom = parseString(req.data).toprettyxml("\t", "\n", None)
                        d = xmltodict.parse(dom, xml_attribs=True)
                        #dicomanifest.update(ast.literal_eval(json.dumps(d).replace("@", "")))
                        fichierconverted = self.convert(file)
                        print("Fichier SMOOTH --> Conversion en Flux Json ...")
                        print("Nouveau Chemin : " + fichierconverted)
                        TT = Traiter(fichierconverted)
                        bodyJSON = TT.generateFlux(timeM.strftime("%Y-%m-%dT%H:%M:%S%Z"), commandchoisi.upper(), modechoisi.upper(), noeud.upper(), chaine.upper())
                        print(bodyJSON)
                        TT.pushToDB(bodyJSON)
                        time.sleep(int(self.getIntervalle()))
                    except:
                        #dicomanifest["message"] = str(req.data).replace("'", "")
                        print("Manifest non pris en charge (DASH et HLS) ! ")
            else:
                if str(patern).upper() == "PATERN2":
                    flux = self.makePaternTwo(commandchoisi, modechoisi)
                for edict in flux:
                    tagsManifest = []
                    for cle, valeur in edict.items():
                        print(cle,valeur)
                        tagsManifest.append(valeur)
                        #tagsManifest[cle] = edict.get[cle]
                    print("Chaine == "+ str(tagsManifest[0])[12:])
                    noeud = "Strm"+str(tagsManifest[0])[12:]
                    chaine = str(tagsManifest[3])
                    timeM= datetime.datetime.utcnow()
                    folder = str("manifests/"+ patern + "/" + commandchoisi + "/"+ modechoisi + "/" + noeud)
                    self.creatingFolder(folder)
                    #Le 3 correspond à l'attribut chaine
                    file = folder + "/"+ tagsManifest[3]
                    print(file)
                    urllib.urlretrieve(tagsManifest[2], file )
                    """
                    VALIDATION - TEST - DB
                    """
                    http = urllib3.PoolManager()
                    req = http.request('GET', str(tagsManifest[2]))
                    from xml.dom.minidom import parseString
                    try:
                        dom = parseString(req.data).toprettyxml("\t", "\n", None)
                        d = xmltodict.parse(dom, xml_attribs=True)
                        import ast
                        #dicomanifest.update(ast.literal_eval(json.dumps(d).replace("@", "")))
                        fichierconverted = self.convert(file)
                        print("Fichier SMOOTH --> Conversion en Flux Json ...")
                        print("Nouveau Chemin : " + fichierconverted)
                        TT = Traiter(fichierconverted)
                        bodyJSON = TT.generateFlux(timeM.strftime("%Y-%m-%dT%H:%M:%S%Z"), commandchoisi.upper(), modechoisi.upper(), noeud.upper(), chaine.upper())
                        print(bodyJSON)
                        TT.pushToDB(bodyJSON)
                        time.sleep(int(self.getIntervalle()))
                    except:
                        #dicomanifest["message"] = str(req.data).replace("'", "")
                        print("Manifest non pris en charge (DASH et HLS) ! ")
                else:
                    print("Pas de flux")
                    #return flux
        #return flux
        except Exception as x:
            print(x)
            self.createLogFile(x)

    """ Retourne le résultat de la requete """
    def getCodeRequest(self, url):
        try:
            print(url)
            import urllib.request, urllib.error, urllib.response
            try:
                conn = urllib.request.urlopen(url)
            except urllib.error.HTTPError as e:
                # Return code error (e.g. 404, 501, ...)
                return e.code
            except urllib.error.URLError as e:
                # Not an HTTP-specific error (e.g. connection refused)
                return "URLError"
            else:
                # 200
                return 200
        except Exception as x:
            print(x)


    """ Conversion du Manifest en  flux JSON et Supprime les at sur les attributs Manifests"""

    def convert(self, manifest, xml_attribs=True):
        try:
            with open(str(manifest), "rb") as f:  # notice the "rb" mode
                d = xmltodict.parse(f, xml_attribs=xml_attribs)
                # print(f)
                # f= json.dumps(d, indent=4)
                fh = open(manifest, 'w')
                fh.writelines(json.dumps(d, indent=4))
                fh.close()
            contenu = ""
            with open(str(manifest), "rb") as fh:  # notice the "rb" mode
                for ligne in fh:
                    contenu += str(ligne).replace("@", "")
                fh.close()
                fichier = open(str(manifest), 'w')
                fichier.write(contenu)
                fichier.close()
            print("Manifest Converti : " + manifest)
            return manifest
        except Exception as x:
            print(x)
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
            self.createLogFile(x)

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
