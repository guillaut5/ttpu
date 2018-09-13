from __future__ import unicode_literals

from django.test import TestCase
from django.test.client import Client
# Create your tests here.
from whowlong.models import Place,Trajet,Request,print_agsp_models
from whowlong.computingtools.calculator import RouteComputer
from django.contrib.auth.models import User

class TestModels(TestCase):
    def setUp(self):
        print u'test_trajet_computing'
        self.routeComputer = RouteComputer()
        


    def test_trajet_computing(self):
        print (u"---------- test_trajet_computing --------------")

        user = User.objects.create_user(username='testuser', password='12345')
        
        print (u'premiere request')
        request= self.routeComputer.initRequest(user, '80 rue jean antoine injalbert 34130 castelnau le lez', 2500, label=u'chezmoi')
        print_agsp_models()    
        
        
        self.routeComputer.buildTrajetsList(request)
        print_agsp_models()    
        
        
        self.assertEqual(len (Trajet.objects.all()),30) 
       
        print request.origin
        print ("recherche dans la base avec un filtre")    
        
        
        
        
        justic = Place.objects.get(name=u'MONTPELLIER AV DE LA JUSTICE')   
        antig = Place.objects.get(name=u'MONTPELLIER ANTIGONE') 
        ml = list()
        ml.append(justic)
        ml.append(antig)
        #trajets = Trajet.objects.filter(name="MONTPELLIER ANTIGONE => MONTPELLIER AV DE LA JUSTICE")
        trajets = Trajet.objects.filter(fromPlace=request.origin).filter(toPlace__in=ml)
        self.assertEqual(len (trajets),2) 
        print ('******************************************************')
        
        for elem in trajets :
            print elem
        
        print ('******************************************************')
        
        for plt in request.places.all() :
            print plt
       
        
        print ('******************************************************')
        print ('Computing...')
        self.routeComputer.computeTrajetLength(request)
            
            
        print ("End of program")        
    
    
     