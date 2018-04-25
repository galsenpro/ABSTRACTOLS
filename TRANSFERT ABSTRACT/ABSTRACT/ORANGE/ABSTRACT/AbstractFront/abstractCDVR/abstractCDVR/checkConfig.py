#!/usr/bin/env python

import os
import settings
import mysql.connector
import json
import errno

def getDBparams(attribute, typedatabase ='default'):
    try:
       # print(settings.DATABASES.get(typedatabase).get(attribute))
        return settings.DATABASES.get(typedatabase).get(attribute)
    except Exception as x:
        return {}

def openFileFromPath(path):
    try:
        fichier = open(path, "r")
        contenu =  fichier.readlines()
        fichier.close()
        c = ""
        for e in contenu:
            c = c + e
        ct =  json.loads(c)
        #print(json.dumps(ct))
        return ct
    except Exception as x:
        print(x)

def checkNewConfig():
    try:
        database =   getDBparams('NAME')
        user =   getDBparams('USER')
        passwd = getDBparams('PASSWORD')
        host =   getDBparams('HOST')
        #port =   getDBparams('PORT')
        conn = mysql.connector.connect(host=host,
                                            user=user,
                                            password=passwd,
                                            database=database)
        cursor = conn.cursor()
        configs = {}
        media = settings.MEDIA_URL
        project = settings.PROJECT_ROOT
        cursor.execute(""" SELECT * FROM `abstract_configurationfile` ORDER BY id DESC LIMIT 0,1 """)
        rows = cursor.fetchall()
        for row in rows:
            configs["name"]  = str(row[1])
            configs["protocole"]  = str(row[2])
            configs["port"]  = str(row[3])
            configs["intervalle"]= str(row[4])
            configs["emailFrom"]= str(row[5])
            configs["smsFrom"]= str(row[6])
            configs["schemasmooth"]= str(row[7])
            configs["schemadash"]= str(row[8])
            configs["nameOfLevelFile"]  = str(row[9])
            configs["folderOfLevelFile"] = str(row[10])
            configs["nameOfIframeFile"] = str(row[11])
            configs["folderOfIframeFile"] = str(row[12])
            configs["livefoldersmooth"] = str(row[13])
            configs["catchupfoldersmooth"] = str(row[14])
            configs["livefolderdash"] = str(row[15])
            configs["catchupfolderdash"] = str(row[16])
            configs["livefolderhls"] = str(row[17])
            configs["catchupfolderhls"] = str(row[18])
            configs["logdirectory"] = str(row[19])
            configs["logprefixname"] = str(row[20])
            configs["created"] = str(row[21])
            path = str(project+media+str(row[22]))
            #print(path)
            #configs["file"] = openFileFromPath(path)
            configs["vspp_id"] = row[23]
            openFileFromPath(path)
            configs.update(openFileFromPath(path))
            myconfigFile =  json.dumps(configs, indent=4, sort_keys=True)
            try:
                fmt = '%Y%m%dT%H%M%S%ZZ'
                dateLog = row[21]
                datecreated = dateLog.strftime(fmt)
                filename = str(project+media)+str(datecreated) +".json"
                if not os.path.exists(os.path.dirname(filename)):
                    try:
                        os.makedirs(os.path.dirname(filename))
                    except OSError as exc: # Guard against race condition
                        if exc.errno != errno.EEXIST:
                            raise
                with open(filename, "w") as f:
                    f.writelines(str(myconfigFile)+"\n")
                    #print str(filename)
                    return str(filename)
            except IOError:
                print("Fichier configs introuvable ! ")
    except Exception as x:
        return "NULL"