# -*- coding: utf-8 -*-
""" Les bureaux de poste"""
import requests
import logging
from whowlong.models import Place
import re
class LaPosteApi(object):
    """ Retourne les point relais ou les bureaux de poste a procximité d'un point GPS"""
    
    LAPOSTE_URL="https://datanova.legroupe.laposte.fr/api/records/1.0/"
    
    def __init__(self,log_lvl=logging.INFO):
        self.log = logging.getLogger(__name__)
        if log_lvl is None:
            log_lvl = logging.WARNING
        self.log.setLevel(log_lvl)
        if not len(self.log.handlers):
            self.log.addHandler(logging.StreamHandler())
        
    def getBureauxPosteArroundThisPoint (self,lat,lon,distance):
        """ return adress of postal office around a point"""
        get_postaloffice=u"search/"
        url_options = {
            u"dataset":u'laposte_poincont2',
            u"facet":u'caracteristique_du_site',
            u"facet":u'code_postal',
            u"facet":u'localite',
            u"facet":u'code_insee',
            u"facet":u'precision_du_geocodage',
            u"facet":u'precision_du_geocodage',
            u"rows":u'1000',
            u"geofilter.distance":u'%f,%f,%f' % (lat,lon,distance)
            }
        
        response = requests.get(self.LAPOSTE_URL + get_postaloffice, params=url_options)
        response_json = response.json()
        places = list()
        for record in response_json['records'] :
            
            place,created = Place.objects.get_or_create(lat=record[u'fields'][u'latitude'],lon=record[u'fields'][u'longitude'])
            #if created :
            #    self.log.info("A new place has been created by laPosteApi")
            place.name = record[u'fields'][u'libelle_du_site']
            '''
            substitue Boite postale et Agence Postale
            MUDAISON BP => MUDAISON 
             SAUSSAN AP => SAUSSAN
             CALVISSON LES JOUETS DE LEO RP => CALVISSON LES JOUETS DE LEO
                         '''
            
            place.name = re.sub('\ BP$', '', place.name)
            place.name = re.sub('\ AP$', '', place.name)
            place.name = re.sub('\ RP$', '', place.name)
            place.name = re.sub('\ LPRT$', '', place.name)

            place.label = place.name
            place.city = record[u'fields'][u'localite']
            
            if u'adresse' in record[u'fields'] and record[u'fields'][u'adresse'] != u"LE BOURG" :
                place.street = record[u'fields'][u'adresse']
                place.postalAdress = "%s %d %s" % (place.street, int(record[u'fields'][u'code_postal']), record[u'fields'][u'localite'])
            else :
                place.street = u''
                place.postalAdress = "%s %s" % (record[u'fields'][u'code_postal'], record[u'fields'][u'localite'])
                
            place.pays = record[u'fields'][u'pays']
            place.lon = record[u'fields'][u'longitude']
            place.lat = record[u'fields'][u'latitude']
            place.save()
            places.append(place)
        self.log.info("found %d places arround %.1f Km" % (len(places), distance/1000))    
        #for place in places :
            #self.log.info(u"  - " + place.name)    
        return places