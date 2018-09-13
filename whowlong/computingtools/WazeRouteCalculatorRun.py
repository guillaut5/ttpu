# -*- coding: utf-8 -*-
from WazeRouteCalculator import WazeRouteCalculator,WRCError
from LaPosteApi import LaPosteApi
from Place import Place
import pandas as pd
#from_address = u'36 allée volta montpellier'
fromAdress = u'500 av georges freche castelnau le lez'
#from_address = u'SAINT MARTIN DE LONDRES'
#from_address = u'lEGE CAP FERRET'

distanceMetre=2000

toAdress = 'école jules simon Montpellier, France'
import operator
import datetime

request = "%dKm autour de %s" %(distanceMetre/1000,fromAdress)


route = WazeRouteCalculator()

startPoint = route.address_to_coords(fromAdress)




laposte = LaPosteApi()
places = laposte.getBureauxPosteArroundThisPoint(startPoint['lat'], 
                                                 startPoint['lon'], 
                                                 distanceMetre)
startPlace = Place()
startPlace.name="Origin"
startPlace.city=startPoint[u'city']
startPlace.street=  u'%s %s' % (startPoint[u'number'],startPoint[u'street'])
startPlace.pays=startPoint[u'city']
startPlace.lon = startPoint[u'lon']
startPlace.lat = startPoint[u'lat']
places.append(startPlace)
print u'Votre lieu : %s' %  fromAdress
totalItineraire=len(places)*(len(places)-1)

print u'Calcul de %d itineraires' % totalItineraire
dictTime = dict()
dictDistance = dict()
trajets=list ()
count = 0
for i, fromPlace in enumerate(places) :
    for j, toPlace in enumerate(places):
        if i != j :
            count=count+1
            date = datetime.datetime.now()
            fromAdress="%s %s" % (fromPlace.street, fromPlace.city)
            fromLabel= fromPlace.name
            toAdress = "%s %s" % (toPlace.street, toPlace.city)
            toLabel = toPlace.name
            try:
                route=WazeRouteCalculator()
                route.init(fromAdress, toAdress)
                
                trajetName="%s => %s" % (fromLabel, toLabel)
                print "[%03d/%03d] trajet %s" % (count,totalItineraire,trajetName)
                route_time, route_distance = route.calc_route_info()
            # suppression des mauvaise adresses trouvées pas Waze
            # par exemple Saint paul de malalle est trouvé a 700km de castelnau...
            # ca va pas...
            # Donc si la distance trouvé par waze> 3 fois la distance a vol d'oiseau
            # on vire
                if route_distance <= distanceMetre*3/1000 :
                    dictTime[trajetName] = route_time
                    dictDistance[trajetName] = route_distance
                    data = dict()
                    data[u'trajet'] = trajetName
                    data[u'trajet_heure']= date.hour
                    data[u'trajet_minute']= round(date.minute,1)
                    data[u'duree_minute']= round(route_time,1)
                    data[u'distance_km'] = round(route_distance,1)
                    data[u'vitesse_kmh'] = int(route_distance/(route_time/60))
                    data[u'fromLabel'] = fromPlace.name
                    data[u'fromCity'] = fromPlace.city
                    data[u'fromAdress'] = fromAdress
                    data[u'fromLat'] = fromPlace.lat
                    data[u'fromLon'] = fromPlace.lon
                    data[u'toLabel'] = toPlace.name
                    data[u'toCity'] = toPlace.city
                    data[u'toAdress'] = toAdress
                    data[u'toLat'] = toPlace.lat
                    data[u'toLon'] = toPlace.lon
                    data[u'request_date'] = date
                    data[u'request_name'] =request
                    trajets.append(data)
                                                 
            
                
            except WRCError as err:
                print err

first = trajets[0]
df= pd.DataFrame(columns=[
                 u'trajet',
                 u'trajet_heure',
                 u'trajet_minute',
                 u'duree_minute',
                 u'distance_km',
                 u'vitesse_kmh',
                 u'fromLabel',
                 u'fromCity',
                 u'fromAdress',
                 u'fromLat',
                 u'fromLon',
                 u'toLabel',
                 u'toCity',
                 u'toAdress',
                 u'toLat',
                 u'toLon',
                 u'request_date',
                 u'request_name'
                 ]
                 )
for data in trajets :
    df=df.append(data, ignore_index=True)
df.to_excel('outputTrajets.xlsx',engine='openpyxl')


sortedTime = sorted(dictTime.items(), key=operator.itemgetter(1))
sortedDistance = sorted(dictDistance.items(), key=operator.itemgetter(1))
date = datetime.datetime.now()
str(date)
print ""
print "origine = %s" % request
print ""
print 'distance en temps'
for key,value in sortedTime :
    print "%02dh%02d : %02d minutes (%02d km/h) pour %s " % (date.hour,date.minute, 
                                                         value, dictDistance[key]/(value/60.0),
                                                         key)

print ""
print 'distance en km'

for key,value in sortedDistance :
    print "%02dh%02d : %02.1f km @ (%02d km/h) pour %s " % (date.hour,date.minute,
                                                      value,value/(dictTime[key]/60.0),
                                                       key)
    
