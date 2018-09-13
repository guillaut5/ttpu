from __future__ import unicode_literals

from django.test import TestCase
from django.test.client import Client
# Create your tests here.
from whowlong.models import Place,Trajet,Request
from whowlong.computingtools.calculator import RouteComputer
from django.contrib.auth.models import User

class TestModels(TestCase):
    def setUp(self):
        print u'test les models'
        self.routeComputer = RouteComputer()
        

    def test_duplicate_coords(self):
        print "---------- test_duplicate_coords --------------"
        place = self.routeComputer.getPlaceFromStringSearch(u'place de la comedie a montpellier')
        
        llong = place.lon
        llat = place.lat 
        place,created = Place.objects.get_or_create(
                 lon =llong,
                lat =llat
                )
        if created:
            print ('new Place created')
        else :
            print ('No place created, a place with the same coord exists')
        self.assertEqual(created,False) 
