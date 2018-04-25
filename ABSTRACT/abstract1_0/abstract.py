#!/usr/bin/python
#-*- coding: utf-8 -*-

from route.RouteConfig import *

if __name__ == "__main__":    
    test = RouteConfig()
    #test.createLogFile("Contenu de mon log")
    while 1:
        links = test.threader(["PATERN1","PATERN2"], ["live", "catchup"], ["smooth","dash", "hls"])
        test.download(links)
        #test.clean(folder)
 