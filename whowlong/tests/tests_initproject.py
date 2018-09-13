from __future__ import unicode_literals

from django.test import TestCase
from django.test.client import Client
# Create your tests here.
from whowlong.models import Place,Trajet
from whowlong.computingtools.calculator import RouteComputer
from django.contrib.auth.models import User

class FirstProjectTestCase(TestCase):
    def setUp(self):
        print u'test de debut de projet'
        self.routeComputer = RouteComputer()
        
        

    def test_getPlaceFromString(self):
        print "---------- TEST getPlaceFromSearch() --------------"
        place = self.routeComputer.getPlaceFromStringSearch(u'place de la comedie a montpellier')
        self.assertEqual(place.lat, 43.60870361328125)  
        place = self.routeComputer.getPlaceFromStringSearch(u'place de la comedie a montpellier')
        self.assertEqual(place.lat, 43.60870361328125) 
        
        origin = place
        placeArround = self.routeComputer.getBureauxDePosteArround(place, 5000)
        
        user = User.objects.create_user(username='testuser', password='12345')
        
        request= self.routeComputer.initRequest(user, '80 rue jean antoine injalbert 34130 castelnau le lez', 7500, label=u'chezmoi')
        print request
        
        
        print ("================")
        request.printPlacesArround()
        
        
        mylist = self.routeComputer.buildTrajetsList(request)
        for elem in mylist :
            print elem
            
        print ("================")
        print request.origin
        print ("recherche dans la base avec un filtre")    
        trajets = Trajet.objects.filter(fromPlace=request.origin)
        for traj in trajets :
            print traj
            
            
        print ("End of program")
        
        