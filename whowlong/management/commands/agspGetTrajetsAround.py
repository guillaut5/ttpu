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
    def add_arguments(self, parser):
        parser.add_argument('--adress', type=str)
        parser.add_argument('--arroundInMeter', type=int)
        
        

    def handle(self, *args, **options):
        start_time =  time.time()
        logger.info(u'Start get trajet arround')
        adress = options['adress']
        logger.info(u'adress:%s '%(adress))
        t0 = time.time()    
        arround = options['arroundInMeter']
        logger.info(u'arround:%sm '%(arround))
        
        routeComputer = RouteComputer()
        user = User.objects.get(username='guillaume')
        request= routeComputer.initRequest(user, '80 rue jean antoine injalbert 34130 castelnau le lez', arround, label=u'CHEZMOIS')
        routeComputer.buildTrajetsList(request)

        
        logger.debug("    objectList,userProfil = agsp.getObjectsList(token) [%06dms] " %(1000*(time.time()-t0)))

        self.stdout.write(self.style.SUCCESS(u'END'))
        
        
        routeComputer.computeTrajetLength(request)

            
            
            
            