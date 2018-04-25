# -*- coding: utf-8 -*-
import mysql.connector
import requests
from lxml import etree
import datetime
import threading
import time
allgo = threading.Condition()


class TestVODAPI(threading.Thread):
    def __init__(self, host = "192.168.134.122", database="abstractvspptest", user="adama", passwd="adama"):
        threading.Thread.__init__(self)
        try:
            self.host = host
            self.database = database
            self.user = user
            self.passwd = passwd
            self.conn = mysql.connector.connect(host=self.host,
                                                user= self.user,
                                                password= self.passwd,
                                                database=self.database)
            self.cursor = self.conn.cursor()
            print ("Trainer ....")
        except Exception as x:
            print(x)

    def disconnect(self):
        try:
            self.conn.close()
        except Exception as x:
            print(x)

    def insertResponse(self, nom, daterequest, link, datareq, status, reason, methode, body, header, duree, typetest = "auto"):
        try:
            resultat = (nom, daterequest, link, datareq, status, reason, methode, body, header, duree, typetest)
            self.cursor.execute("""INSERT INTO abstract_response (nom, daterequest, link, datareq, status, reason, methode, body, header, duree, typetest) VALUES(%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s)""", resultat)
            self.conn.commit()
        except Exception as x:
            print(x)

    def commWithDB(self):
        try:
            self.cursor.execute("""SELECT nom, link, datareq, header FROM abstract_request""")
            rows = self.cursor.fetchall()
            for row in rows:
                nom = row[0]
                link = row[1]
                xml_str = str(row[2])
                root = etree.fromstring(xml_str)
                datareq = etree.tostring(root, pretty_print=True)
                daterequest = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S%Z")
                response = requests.post(str(link), data=datareq, headers={'Content-Type': 'application/xml'})
                link = response.url
                status = response.status_code
                reason = response.reason
                methode = response.request
                headers = response.headers
                duree = response.elapsed
                if response.text == "":
                    body = "Pas de Contenu "
                else:
                    body = response.content
                self.insertResponse(str(nom), str(daterequest), str(link), str(datareq), str(status), str(reason), str(methode), str(body), str(headers), str(duree), "auto" )
                print(nom)
                print(status)
        except Exception as x:
            print(x)

    def run(self):
        try:
            allgo.acquire()
            allgo.wait()
            allgo.release()
            while True:
                self.commWithDB()
                time.sleep(10)
        except:
            pass

for i in range(4):  # Chaque requete sera executée 1 fois (range(1))
    t = TestVODAPI()
    t.start()  # Je lance mes Thread

allgo.acquire()
allgo.notify_all()
allgo.release()
