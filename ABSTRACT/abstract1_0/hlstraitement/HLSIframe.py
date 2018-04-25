#!/usr/bin/python
#-*- coding: utf-8 -*-

#from urllib.request import *
import urllib
import requests
from requests.exceptions import HTTPError

class HLSIframe:
    def __init__(self):
        self.IframeFile = ""
        self.link = ""