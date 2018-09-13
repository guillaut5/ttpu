# -*- coding: utf-8 -*-

'''
Created on 3 mars 2017

@author: guillaume
'''
from django.core.management.base import BaseCommand, CommandError
import time
import logging


from django.test.client import Client
# Create your tests here.
from whowlong.models import Place,Trajet
from whowlong.computingtools.calculator import RouteComputer
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)
from django.http import JsonResponse

class Command(BaseCommand):
    help = u'create trajet arround adress'

    #def add_arguments(self, parser):
        #parser.add_argument('poll_id', nargs='+', type=int)
     #   voir https://stackoverflow.com/questions/27611468/django-management-command-argument 
        
        

    def handle(self, *args, **options):
        start_time =  time.time()
        logger.info(u'Start agsp Waze Miner')
        t0 = time.time()    
        
        routeComputer = RouteComputer()
        trajets = Trajet.objects.all()
        routeComputer.digData(trajets)
                    
            
            
            