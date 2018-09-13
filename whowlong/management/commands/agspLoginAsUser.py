# -*- coding: utf-8 -*-

'''
Created on 3 mars 2017

@author: guillaume
'''
from django.core.management.base import BaseCommand, CommandError
from agsp2smag.core.agsp import A2S_agsp
import time
import logging
from django.contrib.auth.models import User
from agsp2smag.models import UserProfile
from agsp2smag.core.admin import A2S_Admin

logger = logging.getLogger(__name__)
from django.http import JsonResponse

class Command(BaseCommand):
    help = u'login as an user by the web interface, and returns agribase. For test purpose'

    #def add_arguments(self, parser):
        #parser.add_argument('poll_id', nargs='+', type=int)
     #   voir https://stackoverflow.com/questions/27611468/django-management-command-argument 
    def add_arguments(self, parser):
        parser.add_argument('--login', type=str)
        parser.add_argument('--password', type=str)
        

    def handle(self, *args, **options):
        start_time =  time.time()
        logger.info(u'Start Login as')
        login = options['login']
        password = options['password']
        logger.info(u'user:%s password:%s'%(login,password))
        # Start work of the view,as an external web access
        agsp = A2S_agsp()
        if agsp.login(login,password) == True :
            user = User.objects.get(username=login)
            admin = A2S_Admin()
            admin.createEvent(user, 'WEB', 'LOGIN FOR USER %s' % user.username)
            userProfile=UserProfile.objects.get(user=user)
            elapsed_time = time.time() - start_time
            logger.info(u'End login page pour %s [%06dms]'%(login,int(elapsed_time*1000)))
            logger.info( JsonResponse({u'smagToken': '%s' % userProfile.smagToken}) )
            logger.info( JsonResponse({u'agspSessionId': '%s' % userProfile.agspSessionId}) )
            
        else:
            elapsed_time = time.time() - start_time
            logger.info(u'Failed login page pour %s [%06dms]'%(login,int(elapsed_time*1000)))
            return JsonResponse({u'token': u'login Failed'}) 
            
            start_time =  time.time()
            agsp = A2S_agsp()
            agsp.updateDataFromServerTask()
            elapsed_time = time.time() - start_time
            logger.info(u'End Smag transfert [%06dms]'% int(elapsed_time*1000))
            self.stdout.write(self.style.SUCCESS(u'END'))
            
            
            
            