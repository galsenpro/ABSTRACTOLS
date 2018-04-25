#! /usr/bin/python                                                              
# -*- coding: utf-8 -*-                                                         
#                                                                               
# Simple XML validator done while learning the use of lxml library.             
#   -- Adama DIENG >                                  
                                                                                
import lxml                                                                     
from lxml import etree
import sys, os                                                              
                        
                        
class Validation:
    
    def __init__(self):
        self.nom = "dieng"
        
    def ValidationSMOOTH(self, manifest, Validation="profils/dynamic/SMOOTH/SmoothStreamingMedia.xsd"):
       # if len(sys.argv) != 3:                                                      
        #print "Usage: %s document.xml schema.xsd" % (sys.argv[0])               
       # exit(0)                                                                                                                             
        with open(Validation) as f:                                                
            doc = etree.parse(f)   
        #print ("Validating schema ... ")                                              
        try:                                                                        
            schema = etree.XMLSchema(doc)                                           
        except lxml.etree.XMLSchemaParseError as e:                                 
            print (e)                                                                 
            exit(1)                                                                 
        #print ("Schema OK")                                                           
        with open(manifest) as f:                                                
            doc = etree.parse(f)                                                    

        #print ("Validating document ...")                                             
        try:                                                                        
            schema.assertValid(doc)                                                 
        except lxml.etree.DocumentInvalid as e:                                     
            print (e)                                                                
            exit(1)                                                                 

        #print ("Document OK !")

