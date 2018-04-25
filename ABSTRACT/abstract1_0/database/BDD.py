#!/usr/bin/python
#-*- coding: utf-8 -*-
import MySQLdb
import mysql.connector 
class BDD:
    
    def __init__(self, host="192.168.134.122", user="adama", passwd="adama", db="ABSTRACT"):
        try:
            self.db = mysql.connector.connect(host= host, user= user, passwd= passwd, db= db)
            self.cursor = self.db.cursor()
            print "Connected !"
        except Exception as x:
            print "Connexion impossible !"
    
    def commitTransax(self):
        try:
            self.db.commit()
            print "Commit Succed !"
        except Exception as x:
            print "Impossible to commit"
    
    def closeConnection(self):
        try:
            self.db.close()
            print "Closing succed!"
        except Exception as x:
            print "Impossible to close connection!"
    
    def insertStream(self,name_streamer, address, description, idPod):
        try:
            self.cursor.execute("""INSERT INTO streamer VALUES (%s,%s,%s,%s)""",(0,name_streamer,address,idPod))
            print "Insert on Streamer Succed!"
        except Exception as x:
            print "Insert on Streamer Impossible!"
            
    def insertPod(self,name, link, description):
        try:
            self.cursor.execute("""INSERT INTO pod VALUES (%s,%s,%s,%s)""",(0,name,link,description))
            print "Insert on Pod Succed!"
        except Exception as x:
            print "Insert on Pod Impossible!"
            print x
    
    def insertChannel(self,channel, description):
        try:
            self.cursor.execute("""INSERT INTO channels VALUES (%s,%s)""",(0,channel,description))
            print "Insert on Channel Succed!"
        except Exception as x:
            print "Insert on Channel Impossible!"
    
    def insertChunk(self,type_stream, t, d):
        try:
            self.cursor.execute("""INSERT INTO chunks VALUES (%s,%s,%s)""",(0,type_stream,t,d))
            print "Insert on Chunk Succed!"
        except Exception as x:
            print "Insert on Chunk Impossible!"
                 
    def insertPlaying(self,commande,link, file_test, the_mode_id):
        try:
            self.cursor.execute("""INSERT INTO playing VALUES (%s,%s,%s)""",(0,type_stream,t,d))
            print "Insert on Playing Succed!"
        except Exception as x:
            print "Insert on Playing Impossible!"
    
    def insertMode(self,name,abr_static,fragment,suffix_manifest,device_profil,client_version,type_manifest,description):
        try:
            self.cursor.execute("""INSERT INTO mode VALUES (%s,%s,%s,%s,%s,%s)""",(0,type_stream,t,d))
            print "Insert on Playing Succed!"
        except Exception as x:
            print "Insert on Playing Impossible!"
                 
        
    def insertSmoothMedia(self, *param):
        try:
            #self.cursor.execute("""INSERT INTO smooth_streaming_media VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(0,'NomStream', '3', '4', '5', '6', '7', '1', '1', '1', '2016-11-24 07:19:17', '1', 0, '14', '15', '16', '17', '18', '19', '20', '21', '22','23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35'))
            self.cursor.execute("""INSERT INTO smooth_streaming_media VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
 #               (0,'NomStream', '3', '4', '5', '6', '7', '1', '1', '1', '2016-11-24 07:19:17', '1', 0, '14', '15', '16', '17', '18', '19', '20', '21', '22','23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35'))
                (param[0],param[1],param[2],param[3],param[4],param[5],param[6],param[7],param[8],param[9],param[10],param[11],param[12],param[13],param[14],param[15],param[16],param[17],param[18],param[19],param[20],param[21],param[22],param[23],param[24],param[25],param[26],param[27],param[28],param[30],param[31],param[32],param[33],param[34],param[35],param[36],param[37],param[38],param[39],param[40],param[41],param[42],param[43],param[44],param[45],param[45]))
            print "Insert on Smooth Succed!"
        except Exception as x:
            print "Insert on Smooth Impossible!"
            print x
    