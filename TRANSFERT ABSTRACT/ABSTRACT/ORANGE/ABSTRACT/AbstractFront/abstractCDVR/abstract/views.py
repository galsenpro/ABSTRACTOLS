# -*- coding: utf-8 -*-
from django.http import HttpResponse

from django.shortcuts import render, redirect


def home(request):

    """ Exemple de page HTML, non valide pour que l'exemple soit concis """
    return redirect('http://192.168.134.122:3000/dashboard/db/bitrate')

