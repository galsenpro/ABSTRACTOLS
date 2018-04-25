#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Fonction main """

from abstractCDVR.process import *
if __name__ == "__main__":

    for i in range(1):
        t = Process()
        t.start()  # Je lance mes Thread

    allgo.acquire()
    allgo.notify_all()
    allgo.release()