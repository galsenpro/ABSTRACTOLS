#!/usr/bin/python
#-*- coding: utf-8 -*-
#import MySQLdb
import pymysql
import mysql.connector 
class AccessDB:
    """ 
    Initaliasation de la connexion à la base de données 
    """
    def __init__(self, host="192.168.134.122", user="adama", passwd="adama", db="ABSTRACT"):
        try:
            #self.db = mysql.connector.connect(host= host, user= user, passwd= passwd, db= db)
            self.db = pymysql.connect(host= host, user= user, passwd= passwd, db= db)
            self.cursor = self.db.cursor()
            self.response = ()
            print ("Connexion réusie !")
        except Exception as x:
            print ("Connexion impossible !")
            return x
    """ 
    Fonction qui commite les transactions effectuées
    """
    def commitTransax(self):
        try:
            self.db.commit()
            print ("La transaction est bien commitée !")
        except Exception as x:
            print ("Commit impossible")
            return x
    """ 
    Fonction qui ferme la connexion
    """
    def closeConnection(self):
        try:
            self.db.close()
            print ("Fermeture connexion ...")
            print ("Connexion fermée !")
        except Exception as x:
            print ("Impossible to fermer la connexion!")
            return x
    """
    Sélection d'un attribut 
    """
    def selectManifestData(self, value):
        try:            
            print ("Sélection d'un "+value+" dans ManifestData ...")
            #print ("SELECT * FROM manifest_data WHERE attribut = '"+ (value)+"'")
            self.cursor.execute("SELECT * FROM manifest_data WHERE attribut = '"+ (value)+"'")
            self.response = self.cursor.fetchone()
            print (self.response)
            return self.response
        except Exception as e:
            print (e)
            return e
    
    """
    Insertion des attributs SmoothStreamingMedia du manifest
    """
    def insertSmoothAttr(self,tableName, valeur,streamer,dateSup):
        try:
            print ("SmoothStreamingMedia ...")
            print ("Insertion dans "+str(tableName)+" ...")
            #print (0,str(valeur),str(streamer),str(dateSup))
            #print ("INSERT INTO "+tableName+" VALUES (%s,%s,%s,%s)",(0,valeur,streamer,dateSup))
            self.cursor.execute("INSERT INTO "+tableName+" VALUES (%s,%s,%s,%s)",(0,valeur,streamer,dateSup))

        except Exception as e:
            print (e)
            return e
    """
    Insertion des attributs StreamIndex du manifest
    """
    def insertStreamAttr(self,tableName,typeStream, valeur,streamer,dateSup):
        try:
            print ("StreamIndex ...")
            print ("Insertion dans "+str(tableName)+" ...")
            self.cursor.execute("""INSERT INTO """+tableName+""" VALUES (%s,%s,%s,%s)""",(0,typeStream,valeur,streamer,dateSup))

        except Exception as e:
            print (e)
            return e
    """
    Insertion des attributs QualityLevels du manifest
    """
    def insertQltyAttr(self,tableName,typeStream, valeur,streamer,dateSup):
        try:
            print ("QualityLevels ...")
            print ("Insertion dans "+str(tableName)+" ...")
            self.cursor.execute("INSERT INTO "+tableName+" VALUES (%s,%s,%s,%s,%s)",(0,typeStream,streamer,valeur,dateSup))
        except Exception as e:
            print (e)
            return e
    """
    Insertion d'un Streamer
    """              
    def insertStream(self,name_streamer, address, description, idPod):
        try:
            self.cursor.execute("""INSERT INTO streamer VALUES (%s,%s,%s,%s)""",(0,name_streamer,address,idPod))
            print ("Insert on Streamer Succed!")
        except Exception as x:
            print ("Insert on Streamer Impossible!")
            return x
    """
    Insertion d'un Pod
    """  
    def insertPod(self,name, link, description):
        try:
            self.cursor.execute("""INSERT INTO pod VALUES (%s,%s,%s,%s)""",(0,name,link,description))
            print ("Insert on Pod Succed!")
        except Exception as x:
            print ("Insert on Pod Impossible!")
            print (x)
            return x
    """ 
    Insertion d'un Pod
    """
    def insertChannel(self,channel, description):
        try:
            self.cursor.execute("""INSERT INTO channels VALUES (%s,%s)""",(0,channel,description))
            print ("Insert on Channel Succed!")
        except Exception as x:
            print ("Insert on Channel Impossible!")
            return x
    """        
    Insertion d'un historique Player
    """             
    def insertPlaying(self,commande,link, file_test, the_mode_id):
        try:
            self.cursor.execute("""INSERT INTO playing VALUES (%s,%s,%s)""",(0,type_stream,t,d))
            print ("Insert on Playing Succed!")
        except Exception as x:
            print ("Insert on Playing Impossible!")
            return x
    """ Insertion d'un Mode de configuration
    """
    def insertMode(self,name,abr_static,fragment,suffix_manifest,device_profil,client_version,type_manifest,description):
        try:
            self.cursor.execute("""INSERT INTO mode VALUES (%s,%s,%s,%s,%s,%s)""",(0,type_stream,t,d))
            print ("Insert on Playing Succed!")
        except Exception as x:
            print ("Insert on Playing Impossible!")
            return x
    
    """
    Partie Monitoring
    """
    def insertMonitoring(self, *params):
        try:
            print ("Monitoring "+ params[0]+ " ...")
            self.cursor.execute("""INSERT INTO monitoring VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(0,param[0],param[1],param[2],param[3],param[4],param[5],param[6],param[7],param[8]))
        except Exception as x:
            print ("Monitoring : "+x)
            return x
    """        
myInstance = AccessDB("192.168.134.122", "adama", "adama", "ABSTRACT")
myInstance.selectManifestData("MajorVersion")
myInstance.selectManifestData("Bitrate")
myInstance.insertSmoothAttr("major_version", "2", "STREAMER65", "2017-01-06 09:29:42")
myInstance.commitTransax()
myInstance.closeConnection()  
    """