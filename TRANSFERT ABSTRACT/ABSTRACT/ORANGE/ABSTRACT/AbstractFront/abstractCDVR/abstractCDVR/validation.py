#! /usr/bin/python                                                              
# -*- coding: utf-8 -*-    
                                                                               
import lxml                                                                     
from lxml import etree

class Validation:
    
    def __init__(self):
        self.nom = "abstract project"
        self.schema = ""
        
    def ValidationSMOOTH(self, manifest, Validation="profils/dynamic/SMOOTH/SmoothStreamingMedia.xsd"):                                                                                                                           
        with open(Validation) as f:                                                
            doc = etree.parse(f)   
        #print ("Validating schema ... ")                                              
        try:                                                                        
            self.schema = etree.XMLSchema(doc)
        except lxml.etree.XMLSchemaParseError as e:                                 
            print (e)                                                                 
            exit(1)                                                                 
        #print ("Schema OK")                                                           
        with open(manifest) as f:                                                
            doc = etree.parse(f)                                                    
        #print ("Validating document ...")                                             
        try:
            self.schema.assertValid(doc)
        except lxml.etree.DocumentInvalid as e:
            print (e)
            exit(1)
        #print ("Document OK !")

