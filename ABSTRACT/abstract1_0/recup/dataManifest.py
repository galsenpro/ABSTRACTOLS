#!/usr/bin/python
#-*- coding: utf-8 -*-

from lxml import etree                                                                                
import lxml             
import sys, os  

class DataManifestMSS:

    def __init__(self, manifest="Manifest.xml", schema = "profils/static/SMOOTH/SmoothStreamingMedia.xsd"):
        self.file = manifest
        self.schema = schema
        self.tree = etree.parse(manifest)
        self.typeMedia = ""
        self.StreamIndex = {}
        self.QualityLevel = {}
    
    def validSchema(self):                                                        
        with open(self.schema) as f:
            valid = False                                             
            self.tree = etree.parse(f)                                    
        try:                                                                        
            self.schema = etree.XMLSchema(self.tree)
            valid = True  
            #print ("Schema is valid")                                          
        except lxml.etree.XMLSchemaParseError as e:
            valid = False
            print ("Schema incorrect!")                              
        return valid
    
    def validManifest(self):
        if self.validSchema():
            with open(self.file) as f:
                valid = False                                                
                self.tree = etree.parse(f)                                                    
            try:                                                                        
                self.schema.assertValid(self.tree)
                valid = True
                #print ("Manifest is valid")                                             
            except lxml.etree.DocumentInvalid as e:    
                valid = False  
                print ("Manifest incorrect!")
                print (e)                                                                   
            return valid
        else:
            return False
    
    """View all dictionary contents"""
    def viewDictionary(self,fiche):
        try:
            for cle,valeur in fiche.items():
                print (cle, valeur)
            print ("\n")
            #print(fiche.items())
        except Exception as x:
            print (x)
            return x
    """View all list contents"""
    def viewList(self,liste):
        try:
            for element in liste:
                print (element)
        except Exception as x:
            print (x)
            
    """Attribute of SmoothStreamingMedia"""
    
    def getAttribSmoothStreamingMedia(self, attribute =None):
        try:
            if attribute ==None:
                dico = {}
                for smooth in self.tree.xpath("/SmoothStreamingMedia"):
                    dico = smooth.attrib
                #print (dico)
                return smooth.attrib
            else:
                for smooth in self.tree.xpath("/SmoothStreamingMedia"):
                    if smooth.get(attribute)==None:
                        #print ("Indispo")
                        return "Indispo"
                    else:
                        #print (attribute + " -> " + smooth.get(attribute))
                        return smooth.get(attribute)
                print ("\n")
                return smooth.get(attribute)
        except Exception as x:
            print (x)
            return x
    
    
    def getStreamIndexAttribute(self, typeStrIndex, attrStrm):
        liste = []
        try:
            for strm in self.tree.xpath('/SmoothStreamingMedia/StreamIndex[@Type="'+typeStrIndex+'"]'):
                return strm.get(attrStrm)
            else:
                #print ("Erreur")
                return "Erreur "
        except Exception as x:
            print (x)
         
    
    def getValueOfAttributeSmooth(self, dico , attribut = None):
        try:
            if attribut == None:
                for cle,valeur in dico.items():
                    print (cle, valeur)
            else:
                if dico.has_key(str(attribut)):
                    #print (dico.get(str(attribut)))
                    return dico.get(str(attribut)) 
        except Exception as x:
            print (x)   
    
    def getAttribStreamIndex(self, typeStrIndex):
        try:
            liste = []
            for attrStrm in self.tree.xpath('/SmoothStreamingMedia/StreamIndex[@Type="'+typeStrIndex+'"]'):
                liste.append(attrStrm.attrib)
            #print liste
            return liste
        except Exception as x:
            print (x)
    
    def getChunksAttribute(self, typeStrIndex, attrChunks):
        try:
            #print (typeStrIndex +" - "+ attrChunks)
            Valeurs = []
            for chunk in self.tree.xpath('/SmoothStreamingMedia/StreamIndex[@Type="'+typeStrIndex+'"]/c'):
                if chunk.get(attrChunks) != None:
                    Valeurs.append(chunk.get(attrChunks))
            #print Valeurs
            #print ":".join(Valeurs)
            #return ":".join(Valeurs)
            #print Valeurs
            return Valeurs
        except Exception as x:
            print (x)
              
    def getQualityLevelAttribute(self, typeStrIndex, attrQly=None):
        try:
            #print (typeStrIndex)
            Valeurs = []
            for qly in self.tree.xpath('/SmoothStreamingMedia/StreamIndex[@Type="'+typeStrIndex+'"]/QualityLevel'):
               # Valeurs.append(qly.get(attrQly))
                Valeurs.append(qly.attrib)
                #print(qly.attrib)
            #print attrQly + ";" .join(Valeurs)
            #return ":".join(Valeurs)
            return Valeurs
            #print Valeurs
        except Exception as x:
            print (x)
            return x
          
    """Getting the all type of StreamIndex"""
           
    def getTypeStreamIndex(self):
        try:
            listType =  []
            for strm in self.tree.xpath("/SmoothStreamingMedia/StreamIndex"):
                listType.append(strm.get('Type'))
            #print (listType)
            return listType
        except Exception as x:
            print (x)
    def TypeStreamIndexIsPresent(self, liste):
        try:
            if len(liste)!=2:
                print ("Manifest incorrect !")
        except Exception as x:
            print (x)
   
    def validDoc(self):                                                           
        with open(self.schema) as f:                                                
            self.tree = etree.parse(f)                                           
        try:                                                                        
            schema = etree.XMLSchema(self.tree)                                           
        except lxml.etree.XMLSchemaParseError as e:                                 
            print (e)                                                                 
            exit(1)                                                                 
        print ("Schema xsd is OK")                                                           

        with open(self.file) as f:                                                
            self.tree = etree.parse(f)                                                    
        try:                                                                        
            schema.assertValid(self.tree)                                                 
        except lxml.etree.DocumentInvalid as e:                                     
            print (e)                                                                 
            exit(1)                                                                 
        #print ("Manifest file is OK")
    
    def testValueOfAttribute(self, listing, valueOfTest):
        dico = {}
        for element in listing:
            if element < valueOfTest:
                key = listing.index(element)
                valeur = element +" inférieur à" + valueOfTest
                dico[key] = valeur
        #print (dico)
        return dico

                
                 