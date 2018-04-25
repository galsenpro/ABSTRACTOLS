# -*- coding: utf-8 -*-

import threading
import time
from route import *
#Importer le module training.py  pour faire la VOD | nPVR
from checkConfig import *
allgo = threading.Condition()

class Process(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def execution(self):
        """ Recupération des paramètres définis dans le fichier de configuration """
        config = checkNewConfig()
        """ Définition des routes Manifests """
        abstract = RouteConfig(config)
        """ Exécution des Paterns """
        abstract.threader(["PATERN1", "PATERN2"], ["live", "catchup"], ["smooth", "dash", "hls"])
        """ Niveau de tests VOD | nPVR """
        #objVODouNPVR = NomClasseVODouNPVR
        #objVODouNPVR.threader(....)
        

    def run(self):
        try:
            allgo.acquire()
            allgo.wait()
            allgo.release()
            while True:
                self.execution()
                time.sleep(2)
        except:
            pass
