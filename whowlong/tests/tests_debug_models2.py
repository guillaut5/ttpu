from __future__ import unicode_literals

from django.test import TestCase
from django.test.client import Client
# Create your tests here.
from whowlong.models import Place,Trajet,Request,print_agsp_models
from whowlong.computingtools.calculator import RouteComputer
from django.contrib.auth.models import User

class TestModels(TestCase):
    def setUp(self):
        print u'test les models'
        self.routeComputer = RouteComputer()
        


    def test_duplicate_place_after_request(self):
        print (u"---------- test_duplicate_place_after_request 1500m --------------")

        user = User.objects.create_user(username='testuser', password='12345')
        
        print (u'premiere request')
        request= self.routeComputer.initRequest(user, '80 rue jean antoine injalbert 34130 castelnau le lez', 1500, label=u'chezmoi')
        print_agsp_models()    
        
        print ('seconde requests')
        request= self.routeComputer.initRequest(user, '80 rue jean antoine injalbert 34130 castelnau le lez', 1500, label=u'chezmoi')
        print_agsp_models()
         
        self.assertEqual(len (Place.objects.all()),3) 
        
        
        self.routeComputer.buildTrajetsList(request)
        print_agsp_models()
        
        self.routeComputer.buildTrajetsList(request)
        print_agsp_models()
        
        
        self.assertEqual(len (Trajet.objects.all()),6) 
        
    def test_duplicate_place_after_request_bigger_radius(self):
        print (u"---------- test_duplicate_place_after_request_bigger_radius 8000m --------------")

        user = User.objects.create_user(username='testuser', password='12345')
        
        print (u'premiere request')
        request= self.routeComputer.initRequest(user, '80 rue jean antoine injalbert 34130 castelnau le lez', 8000, label=u'chezmoi')
        print_agsp_models()    
        
        print ('seconde requests')
        request= self.routeComputer.initRequest(user, '80 rue jean antoine injalbert 34130 castelnau le lez', 8000, label=u'chezmoi')
        print_agsp_models()
         
        self.assertEqual(len (Place.objects.all()),35) 
        
        
        self.routeComputer.buildTrajetsList(request)
        print_agsp_models()
        
        self.routeComputer.buildTrajetsList(request)
        print_agsp_models()
        
        
        self.assertEqual(len (Trajet.objects.all()),1190)
        #print ('build trajet list')
        #self.routeComputer.buildTrajetsList(request)
        #self.printAll()    
        