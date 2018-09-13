# -*- coding: utf-8 -*-
"""Waze route calculator"""
import sys
import logging
import requests

from whowlong.computingtools.WazeRouteCalculator import WazeRouteCalculator,WRCError

from whowlong.computingtools.LaPosteApi import LaPosteApi
from whowlong.models import Place,Request,Trajet,TrajetData
from pywin.scintilla.find import SearchParams
from datetime import datetime
from django.utils.timezone import now
from random import shuffle

class RouteComputer(object):
    
    
    def __init__(self,log_lvl=logging.INFO):
        self.log = logging.getLogger(__name__)
        if log_lvl is None:
            log_lvl = logging.WARNING
        self.log.setLevel(log_lvl)
        if not len(self.log.handlers):
            self.log.addHandler(logging.StreamHandler())
        self.wazeCalculator= WazeRouteCalculator()
        self.laposte = LaPosteApi()
    
    def digData(self, trajets):
        i = 0
        trajets = list(trajets)
        size = len(trajets)
        shuffle(trajets)
        for trj in trajets :
            i = i +1
            route_time, route_distance = self.wazeCalculator.calc_route_info(trj.fromPlace.postalAdress, trj.toPlace.postalAdress)
            self.log.info("[%d/%4d] %-60s %5.1fkm %4.1fmin "% (i,size,trj, route_distance,route_time))
            tmpDate = now()
            object= TrajetData.objects.create(
                trajet=trj,
                distanceKm = route_distance,
                dureeMinute = route_time,
                trajetDateHeure =round(tmpDate.hour,1),
                trajetDateMinute = round(tmpDate.minute,1),
                trajetWeekDay=datetime.today().weekday()
                )
            object.save()
        
        
    def computeTrajetLength(self,request):
        
        trajets = Trajet.objects.filter(fromPlace=request.origin).filter(toPlace__in=request.places.all())
                    #print ("%s %.1fkm %.1fmin"% (trajet.name, route_distance,route_time)) 
        self.digData(trajets)
        
    def buildTrajetsList(self,request):
        rlist = request.places.all()
        rlist = list()
        for i, tmp in enumerate(request.places.all()):
            rlist.append(tmp)
        rlist.append(request.origin)

        returnv =[]

        for fromPlace in rlist :
            for toPlace in rlist:
                #print fromPlace
                if fromPlace.id != toPlace.id :
                    trajet, created = Trajet.objects.get_or_create(
                        fromPlace = fromPlace,
                        toPlace = toPlace)
                    if created == True :
                        trajet.name = "%s => %s" % (fromPlace.name, toPlace.name)
                        trajet.type='CAR'
                        trajet.save()
                    #print fromPlace.postalAdress
                    #print toPlace.postalAdress
                    #print ("%s => %s" % (fromPlace.postalAdress, toPlace.postalAdress))

                    #route_time, route_distance = self.wazeCalculator.calc_route_info(fromPlace.postalAdress, toPlace.postalAdress)
                    #print ("%s %.1fkm %.1fmin"% (trajet.name, route_distance,route_time))
                    returnv.append(trajet)
        return returnv
                        
                        
    
    def initRequest(self, user_p, search, distanceArround=5000, label=None):
        request,created = Request.objects.get_or_create(
            user = user_p,
            metersArround=distanceArround,
            searchPattern=search)
        if created == False :
            self.log.info("The request with search pattern '%s' is already existing"% search)
        
        place=self.getPlaceFromStringSearch(search)
        place.name = label
        if label != None:
            place.name = label
        else:
            place.name = place.postalAdress
        place.save()
        request.origin  = place
        request.name = "%s arround %d m" % (label,distanceArround)

        
        
        
        self.log.info("Init request around '%s, radio %.1f km."%( place.name, distanceArround/1000.0))
        for tmpPlace in self.getBureauxDePosteArround(request.origin, distanceArround) :
            request.places.add(tmpPlace)
        request.save()

        return request
    
    
    
     

        
    def getBureauxDePosteArround(self, place, radiusInMeters):
        placesList = self.laposte.getBureauxPosteArroundThisPoint(place.lat, place.lon, radiusInMeters)
        
        return placesList
        
        
    def getPlaceFromStringSearch(self,adress="80 rue injalbert 34130 castelnau le lez"):
        point = self.wazeCalculator.getLocationFromAdress(adress)
        if point == None or len (point) ==0:
            self.log.info("No place found for adress [%s]" %  adress)
            return None
        else :
            streetWanted = u''
            if point[u'number'] == None :
                    streetWanted =u'%s' % (point[u'street'])
            else :
                    streetWanted =u'%s %s' % (point[u'number'],point[u'street'])
            place,created = Place.objects.get_or_create(
                postalAdress= u'%s %s' % (streetWanted,point[u'city']),
                street =streetWanted,
                city =point[u'city'],
                lon =point[u'lon'],
                lat =point[u'lat'],
                 )
            if created :
                self.log.info("A new place has been stored : %s" % place.postalAdress)
            else :
                self.log.info("The place  %s is already in the database" % place.postalAdress)
           
            return place
        
        
        
        
            
            

        
    