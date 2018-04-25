#!/usr/bin/python
#-*- coding: utf-8 -*-

#from urllib.request import *
import urllib
import requests
from requests.exceptions import HTTPError

class HLSLevel:
    def __init__(self):
        self.LevelFile = ""
        self.link = ""